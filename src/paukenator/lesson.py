
import re
import random
from collections import defaultdict

from paukenator.prompts import SimplePrompt, InteractivePrompt, \
                               Challenge, MultipleChoiceChallenge
from paukenator.nlp import WordTokenizer

class Lesson(object):
    NOWORD = "..."
    HIDE_RATIO = 0.1

    # type of prompt
    NON_INTERACTIVE  = 1
    INTERACTIVE     = 2
    MULTIPLE_CHOICE = 3

    def __init__(self, text, **kwargs):
        self.text = text
        self.hide_mode = kwargs.get('hide_mode', 'full')
        self.hide_ratio = kwargs.get('hide_ratio', self.HIDE_RATIO)
        self.prompt_mode = kwargs.get('interactive', None) or self.NON_INTERACTIVE
        self.prompt = None
        self.wtok = None
        self.counts = defaultdict(int)

    def run(self):
        self.prompt = self._create_prompt()
        self.prompt.show_help()

        it = iter(self.text)
        c_curr, c_all = 0, len(it)

        words = None

        while self.prompt.is_running:
            if self.prompt.proceed:
                try:
                    line = next(it)
                    c_curr += 1
                except StopIteration:
                    break
                if not line:
                    # TODO: we are skipping empty lines but still count them in
                    # c_curr, which may lead to the fact that c_curr may jump
                    # over some numbers
                    continue

                words = self.to_words(line)

            words_with_gaps, hidden_words = self.hide_words(words)
            self.prompt.hidden_words = hidden_words

            # show the challenge
            # TODO: move this into Prompt?
            print(f"----- Sentence {c_curr} of {c_all} -----")
            print(" ".join(words_with_gaps))
            self.counts['sentences'] += 1

            # process user input
            self.prompt.run()

            # show answer (full sentence)
            print(" ".join(words))
            print()

        self.update_stats()
        self.show_stats() # TODO: depends on the Prompt

        self.prompt.goodbye()

    def hide_words(self, words):
        positions = [idx for idx,wd in enumerate(words)
                        if not self.must_be_visible(wd)]
        if self.hide_ratio:
            size = int(len(positions) * self.hide_ratio) or 1
        hidden_positions = sorted(random.sample(positions, k=size))

        words_with_gaps = list(words)
        hidden_words = []
        for idx,widx in enumerate(hidden_positions):
            hidden_word = self.hide_word(words[widx], idx)
            words_with_gaps[widx] = hidden_word
            hidden_words.append((widx, words[widx], hidden_word))

        return words_with_gaps, hidden_words

    def hide_word(self, word, idx):
        """Transform given :word to hidden representation (aka "gap", "blank").
        In its basic form, hidden representation is just ellipsis:
          * computer --> ...
        but can also be partially hidden, e..g
          * computer --> c..r
          * tie      --> t..
        In any of interactive modes, it is useful to include a number into such
        hidden representation to ensure that the are non-ambiguously indendified
        in case there are more than one gap in a single sentence:
          * computer --> <<1 c..r >>  (partially hidden)
          * tip      --> <<5 ... >>   (fully hidden)
        The gaps are numbered starting from 1 to make it human-friendly.

        TODO: select randomly which characters will be kept visible?
        """
        gap = self.NOWORD
        if self.hide_mode == 'partial':
            if len(word) > 3:
                gap = word[0] + self.NOWORD + word[-1] # c..r
            else:
                gap = word[0] + self.NOWORD[0:2] # t..
        if self.is_interactive:
            # ex: <<2 ... >> or <<2 A...e >>
            gap = f"<<{idx+1} {gap} >>"
        return gap

    def must_be_visible(self, word):
        """
        Tell if given :word should never be hidden from a sentence. Such words
        include:
         * punctuation marks
         * words that are also prompt commands
        """
        return re.match(r'\W+', word) or word in self.prompt.COMMANDS.keys()

    @property
    def is_interactive(self):
        """Tell if the current prompt mode is one of interactive modes or not"""
        return self.prompt_mode in (self.INTERACTIVE, self.MULTIPLE_CHOICE)

    def _create_prompt(self):
        """Create and return prompt according to the current prompt mode."""
        if self.prompt_mode == self.NON_INTERACTIVE:
            prompt = SimplePrompt()
        elif self.prompt_mode == self.INTERACTIVE:
            prompt = InteractivePrompt()
            prompt.challenge_class = Challenge
        elif self.prompt_mode == self.MULTIPLE_CHOICE:
            prompt = InteractivePrompt()
            prompt.text = self.text # will be used by MultipleChoiceChallenge
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

    def to_words(self, string):
        """Tokenize given text string"""
        if self.wtok is None:
            self.wtok = WordTokenizer(lang=self.text.lang)
        return self.wtok(string)
