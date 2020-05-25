
class Exercise(object):
    """Base class for any type of exercise"""

    @classmethod
    def description(cls):
        return "basic exercise"

    def __init__(self, sentence):
        self.hidden_words = None
        self.sentence = sentence

    @property
    def sentence(self):
        return self._sentence

    @sentence.setter
    def sentence(self, sent):
        self._sentence = sent

    def __str__(self):
        return self.sentence
