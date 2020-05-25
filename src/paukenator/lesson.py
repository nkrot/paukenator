import re
from collections import defaultdict

from paukenator.prompts import SimplePrompt, InteractivePrompt
from paukenator.prompts.challenges import Challenge, MultipleChoiceChallenge
from paukenator.exercises import FillInTheGaps
from paukenator.report import Report


class Lesson(object):
    HIDE_RATIO = 0.1

    # type of prompt
    NON_INTERACTIVE = 1
    INTERACTIVE     = 2
    MULTIPLE_CHOICE = 3

    def __init__(self, text, config, **kwargs):
        self.text = text
        self.config = config
        self.prompt_mode = self.config.testmode
        self.selector = self.config.selector

        self.prompt = None
        self.counts = defaultdict(int)

    def run(self):
        self.prompt = self._create_prompt()
        self.prompt.start()

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

            self.prompt.exercise = self._create_exercise(sentence)

            # show the exercise
            # TODO: move this into Prompt or Exercise?
            msg = "----- Sentence {} of {} (sentence #{} of {}) -----"
            print(msg.format(c_curr, c_all, 1+sentence.num, num_sents_in_text))
            print(self.prompt.exercise)

            # process user input
            self.prompt.run()

            # show the correct answer (full sentence)
            print(sentence)
            print()

        self.prompt.finish()
        print(self.prompt.report)

        self.prompt.goodbye()

    def _create_exercise(self, sentence):
        return FillInTheGaps(sentence, self.config,
                             number_gaps=self.prompt.is_interactive,
                             exceptions=self.prompt.COMMANDS.keys())

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
            # here: we create a half-baked MultipleChoiceChallenge() with .text
            # and then create any new real Challenge by copying the prototype.
            # Alternatively, something like Factory Method, e.g.
            # MultipleChoiceChallengeMaker(text) with create_challenge() method
            prompt = InteractivePrompt()
            prompt.text = self.text  # will be used by MultipleChoiceChallenge
            prompt.challenge_class = MultipleChoiceChallenge
        else:
            raise ValueError(f"Unknown prompt mode: {self.prompt_mode}")
        # TODO: the order of setting attributes is important: report must be
        # the last one to set, at least after challenge_class has been set.
        prompt.report = Report()
        prompt.report.text = self.text
        return prompt

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
