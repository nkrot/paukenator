
import re
import random
from collections import defaultdict

from paukenator.prompts import SimplePrompt, InteractivePrompt
from paukenator.nlp import WordTokenizer

class Lesson(object):
    NOWORD = "..."
    HIDE_RATIO = 0.1

    def __init__(self, text, **kwargs):
        self.text = text
        self.hide_mode = kwargs.get('hide_mode', 'full')
        self.hide_ratio = kwargs.get('hide_ratio', self.HIDE_RATIO)
        self.interactive = kwargs.get('interactive', False)
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
                    # TODO: we are skipping empty lines but still count them in c_curr,
                    # which may lead to the fact that c_curr may jump over some numbers
                    continue

                words = self.to_words(line)

            words_with_gaps, hidden_words = self.hide_words(words)
            self.prompt.hidden_words = hidden_words

            # show the challenge
            print(f"----- Sentence {c_curr} of {c_all} -----")
            print(" ".join(words_with_gaps))
            self.counts['sentences'] += 1

            # process user input
            self.prompt.read_input()

            # show answer (full sentence)
            print(" ".join(words))
            print()

        self.update_stats()
        self.show_stats()

        self.prompt.goodbye()

    def hide_words(self, words):
        positions = [idx for idx,wd in enumerate(words) if not self.must_be_visible(wd)]
        if self.hide_ratio:
            size = int(len(positions) * self.hide_ratio) or 1
        hidden_positions = sorted(random.sample(positions, k=size))

        words_with_gaps = list(words)
        hidden_words = []
        for idx,widx in enumerate(hidden_positions):
            words_with_gaps[widx] = self.hide_word(words[widx], idx)
            hidden_words.append((widx, words[widx]))

        return words_with_gaps, hidden_words

    def to_words(self, string):
        if self.wtok is None:
            self.wtok = WordTokenizer(lang=self.text.lang)
        return self.wtok(string)

    def hide_word(self, word, idx):
        # TODO: select randomly which characters will be kept visible?
        res = self.NOWORD
        if self.hide_mode == 'partial':
            if len(word) > 3:
                res = word[0] + self.NOWORD + word[-1]
            else:
                res = word[0] + self.NOWORD[0:2]

        if self.interactive:
            # Gaps in interactive mode are numbered (for better readability, starting from 1)
            # <<2 ... >> or <<2 A...e >>
            res = f"<<{idx+1} {res} >>"

        return res

    def must_be_visible(self, word):
        """
        Tokens like punctuation marks and reserved prompt commands should never
        be hidden from a sentence.
        """
        return re.match(r'\W+', word) or word in self.prompt.COMMANDS.keys()

    def _create_prompt(self):
        if self.interactive:
            prompt = InteractivePrompt()
        else:
            prompt = SimplePrompt()
        return prompt

    def update_stats(self):
        self.counts.update({
            'correct answers'  : self.prompt.counts['correct'],
            'received answers' : self.prompt.counts['answered']
        })

    def show_stats(self):
        msgs = [
            f"Sentences shown: {self.counts['sentences']}",
            f"Answers received/correct: {self.counts['received answers']}/{self.counts['correct answers']}"
        ]
        print("\n".join(msgs))
