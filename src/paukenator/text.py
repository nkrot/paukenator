"""
"""
from collections import Counter

class Text(object):

    @classmethod
    def load(cls, fname, **kwargs):
        text = cls()
        with open(fname) as fd:
            text.lines = fd.read().split('\n')
        text.lang = kwargs.get('lang', 'deu')
        return text

    @classmethod
    def is_comment(cls, line):
        return line.startswith('#')

    def __init__(self):
        self.lines = []
        self.lang = 'deu'
        self.skip_comments = True
        self._wordcounts = None

    def __iter__(self):
        return self.LinesIterator(self)

    def is_empty(self):
        return len(self.lines) == 0

    @property
    def wordcounts(self):
        if self._wordcounts is None:
            self._wordcounts = Counter()
            for line in self.lines:
                if not self.is_comment(line):
                    # TODO: tokenize in a smarter way. also in Lesson.to_words
                    words = line.split()
                    self._wordcounts.update(words)
        return self._wordcounts

    class LinesIterator(object):
        def __init__(self, text):
            self.text = text
            self.items = self.text.lines
            self.idx = -1
            self.last_idx = len(self.items) - 1

        @property
        def items(self):
            return self._items

        @items.setter
        def items(self, lst):
            """ Preselect valid lines """
            self._items = [(idx,item) for idx,item in enumerate(lst) if self._is_valid(item)]

        def __len__(self):
            return len(self.items)

        def __iter__(self):
            return self

        def __next__(self):
            self.idx += 1
            if self.idx <= self.last_idx:
                _, item = self.items[self.idx]
                return item
            raise StopIteration

        def _is_valid(self, line):
            return not self.text.skip_comments or not self.text.is_comment(line)
