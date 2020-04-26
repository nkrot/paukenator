
import re
import random

from paukenator.nlp import WordTokenizer

class Lesson(object):
    NOWORD = "..."

    def __init__(self, text):
        self.text = text
        self.hide_ratio = 0.1
        self.wtok = None

    def run(self):
        # TODO: add info like "showing m-th out of n sentences"
        #msg = "Press q to quit or any other key to continue"
        msg = "Press q to quit, r to repeat or any other key to continue"
        print(msg)

        it = iter(self.text)
        proceed = True

        while True:
            if proceed:
                try:
                    line = next(it)
                except StopIteration:
                    break
                if not line:
                    continue
                words = self.to_words(line)

            words_and_gaps = self.hide_words(words)
            print(" ".join(words_and_gaps))

            proceed = True
            ans = input("> ")

            if ans == 'r':
                proceed = False
                continue

            print(" ".join(words))
            print()

            if ans == 'q':
                break

        self.goodbye()

    def hide_words(self, words):
        positions = [idx for idx,wd in enumerate(words) if not re.match(r'\W+', wd)]
        if self.hide_ratio:
            size = int(len(positions) * self.hide_ratio) or 1
        hidden_positions = random.choices(positions, k=size)

        words_with_gaps = list(words)
        for idx in hidden_positions:
            words_with_gaps[idx] = self.NOWORD

        return words_with_gaps

    def to_words(self, string):
        if self.wtok is None:
            self.wtok = WordTokenizer(lang=self.text.lang)
        return self.wtok(string)

    def goodbye(self):
        print("Good bye. Hope to see you soon again.")