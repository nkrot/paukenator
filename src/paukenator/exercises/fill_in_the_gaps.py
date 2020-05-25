import random

from .hidden_word import HiddenWord
from .exercise import Exercise


class FillInTheGaps(Exercise):

    @classmethod
    def description(cls):
        return "fill in the gaps"

    def __init__(self, sentence, config, **kwargs):
        self.hide_ratio = config.hide_ratio
        self.hide_mode = config.hide_mode
        self.number_gaps = kwargs.get('number_gaps', False)  # for HiddenWord
        self.exceptions = kwargs.get('exceptions', [])
        super().__init__(sentence)  # NOTE: this calls sentence.setter

    @property
    def sentence(self):
        # TODO: why does not this property from base class work?
        return self._sentence

    @sentence.setter
    def sentence(self, sent):
        self._sentence = sent
        self._hide_words()

    def __str__(self):
        return " ".join([str(w) for w in self.words_with_gaps])

    def _hide_words(self):
        """
        TODO: refactor this method to return List[Word or HiddenWord]
        """
        # because can be Word or str. TODO: refactor
        words = [str(wd) for wd in self._sentence.words]
        positions = [idx for idx, wd in enumerate(words)
                         if not self._must_be_visible(wd)]
        if self.hide_ratio:
            size = int(len(positions) * self.hide_ratio) or 1
        hidden_positions = sorted(random.sample(positions, k=size))

        self.words_with_gaps = list(words)
        self.hidden_words = []
        for idx, widx in enumerate(hidden_positions):
            hidden_word = self.hide_word(words[widx], idx)
            self.words_with_gaps[widx] = hidden_word.hidden
            self.hidden_words.append(hidden_word)

    def hide_word(self, text, pos):
        hw = HiddenWord(text, pos, hide_mode=self.hide_mode,
                        include_position=self.number_gaps)
        return hw

    def _must_be_visible(self, word):
        word = str(word)
        return (word in self.exceptions or HiddenWord.is_always_visible(word))
