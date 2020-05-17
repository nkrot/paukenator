import re
import random
from collections import defaultdict

from paukenator import HiddenWord
from paukenator.prompts import SimplePrompt, InteractivePrompt
from paukenator.prompts.challenges import Challenge, MultipleChoiceChallenge


class Lesson(object):
    HIDE_RATIO = 0.1

    # type of prompt
    NON_INTERACTIVE = 1
    INTERACTIVE     = 2
    MULTIPLE_CHOICE = 3

    def __init__(self, text, config, **kwargs):
        self.text = text
        self.config = config
        self.hide_mode = self.config.hide_mode
        self.hide_ratio = self.config.hide_ratio
        self.prompt_mode = self.config.testmode
        self.selector = self.config.selector

        self.prompt = None
        self.counts = defaultdict(int)

    def run(self):
        self.prompt = self._create_prompt()
        self.prompt.show_help()

        sentences = self.selector.select_sentences(self.text)

        c_curr, c_all = 0, len(sentences)
        num_sents_in_text = len(self.text.sentences)
        sentences = iter(sentences)
        sentence = None

        while self.prompt.is_running:
            if self.prompt.proceed:
                try:
                    sentence = next(sentences)
                    c_curr += 1
                except StopIteration:
                    break

            words_with_gaps, hidden_words = self.hide_words(sentence.words)
            # TODO: refactor to accept List[Word or HiddenWord]
            self.prompt.hidden_words = hidden_words

            # show the challenge
            # TODO: move this into Prompt? -- no, not before other types of
            # exercises appear. Prompt should not take too much from Lesson
            msg = "----- Sentence {} of {} (sentence #{} of {}) -----"
            print(msg.format(c_curr, c_all, 1+sentence.num, num_sents_in_text))
            print(" ".join(words_with_gaps))
            self.counts['sentences'] += 1

            # process user input
            self.prompt.run()

            # show the correct answer (full sentence)
            print(sentence)
            print()

        self.update_stats()
        self.show_stats()  # TODO: depends on the Prompt

        self.prompt.goodbye()

    def hide_words(self, words):
        """
        TODO: refactor this method to return List[Word or HiddenWord]
        """
        words = [str(wd) for wd in words]  # because can be Word or str
        positions = [idx for idx, wd in enumerate(words)
                         if not self.must_be_visible(wd)]
        if self.hide_ratio:
            size = int(len(positions) * self.hide_ratio) or 1
        hidden_positions = sorted(random.sample(positions, k=size))

        words_with_gaps = list(words)
        hidden_words = []
        for idx, widx in enumerate(hidden_positions):
            hidden_word = HiddenWord(words[widx], idx,
                                     hide_mode=self.hide_mode,
                                     include_position=self.is_interactive)
            words_with_gaps[widx] = hidden_word.hidden
            hidden_words.append(hidden_word)

        return words_with_gaps, hidden_words

    def must_be_visible(self, word):
        """
        Tell if given :word should never be hidden from a sentence. Such words
        include:
         * words that are also prompt commands
         * other exceptions e.g. punctuation marks
         * TODO: exceptions set from outside?
        """
        word = str(word)
        return (word in self.prompt.COMMANDS.keys()
                or HiddenWord.is_always_visible(word) )

    @property
    def is_interactive(self):
        """
        Tell if the current prompt mode is one of interactive modes or not
        """
        return self.prompt_mode in (self.INTERACTIVE, self.MULTIPLE_CHOICE)

    def _create_prompt(self):
        """Create and return prompt according to the current prompt mode."""
        if self.prompt_mode == self.NON_INTERACTIVE:
            prompt = SimplePrompt()
        elif self.prompt_mode == self.INTERACTIVE:
            prompt = InteractivePrompt()
            prompt.challenge_class = Challenge
        elif self.prompt_mode == self.MULTIPLE_CHOICE:
            # TODO: refactor. If Prompt never uses .text for itself, it should
            # never know about it. Perhaps the pattern Prototype can be applied
            # here: we create a halb-baked MultipleChoiceChallenge() with .text
            # and then create any new real Challenge by copying the prototype.
            # Alternatively, something like Factory Method, e.g.
            # MultipleChoiceChallengeMaker(text) with create_challenge() method
            prompt = InteractivePrompt()
            prompt.text = self.text  # will be used by MultipleChoiceChallenge
            prompt.challenge_class = MultipleChoiceChallenge
        else:
            raise ValueError(f"Unknown prompt mode: {self.prompt_mode}")
        return prompt

    def update_stats(self):
        self.counts.update({
            'correct answers'  : self.prompt.counts['correct'],
            'received answers' : self.prompt.counts['answered']
        })

    def show_stats(self):
        msgs = [
            "Sentences shown: {}".format(self.counts['sentences']),
            "Answers received/correct: {}/{}".format(
                self.counts['received answers'],
                self.counts['correct answers'])
        ]
        print("\n".join(msgs))

    class Selector(object):
        """
        Selectors are 1-based
        Negative indices are not allowed.

        Examples:
        all   -- all sentences
        1..5  -- sentences 1 though 5, both ends included
        4..   -- starting from 4 and till the end
        ..10  -- starting from 1 and till 10 inclusive
        """

        SPEC_REGEXEN = [
            re.compile(r'^(?P<s>[1-9]\d*)\.\.+(?P<e>[1-9]\d*)$'),
            re.compile(r'^(?P<s>[1-9]\d*)\.\.+$'),
            re.compile(r'^\.\.+(?P<e>[1-9]\d*)$'),
        ]

        @classmethod
        def parse_selector_spec(cls, spec):
            """Parse sentence selector specification

            TODO: support more complex cases
            1,3,5..10,20 -- sentences 1, 3, 5 through 10 and sentence 20
            p1..3 -- sentences in paragraphs 1 through 3
            """
            if spec.lower() == 'all':
                return [slice(0, None)]

            for regex in cls.SPEC_REGEXEN:
                m = re.search(regex, spec)
                if m:
                    groups = m.groupdict()
                    s = int(groups.get('s', 1)) - 1
                    e = int(groups['e']) if 'e' in groups else None
                    return [slice(s, e)]

            raise ValueError("Wrong selector specification")

        def __init__(self, spec=None):
            self.spec = spec or 'all'
            self.selectors = None
            if self.spec:
                self.selectors = self.parse_selector_spec(self.spec)

        def select_sentences(self, text):
            """
            Select subset of sentences from text according to the selector or
            all sentences if no selector was congifured.

            Return
            list of sentences
            """
            return self.select_from_list(text.sentences)

        def select_from_list(self, items):
            """
            Select item(s) from the given list <items> according to predefined
            spec and return the selection as a list, even if there is only one
            item.

            TODO
            1. can the selection be empty? return empty list or raise an error
            2. error if out of range?
            """
            if self.selectors:
                selected = []
                for sel in self.selectors:
                    selected.extend(items[sel])
            else:
                selected = items
            return selected

        # def __repr__(self):
        #     return f"{self.__class__.__name__}: {self.spec}"

        def __str__(self):
            return str(self.spec)

        def __eq__(self, other):
            """TODO: well, is it really needed? So far used in tests only"""
            return self.selectors == other.selectors
