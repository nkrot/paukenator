
class Word(object):
    def __init__(self):
        # object being annotated, can be one word before tokenization but
        # should preferably be one sentence
        self.data = None  # str

        # character offset of the span in self.data that corresponds
        # to the current sentence
        self._offsets = None  # (start, end) 0-based

    @property
    def offsets(self):
        return self._offsets

    @offsets.setter
    def offsets(self, ofs):
        assert isinstance(ofs, (tuple, list)), \
            "offsets can be either a tuple or a list of integers"
        assert len(ofs) == 2, "offsets must be a tuple of 2 integers"
        assert ofs[0] <= ofs[1], "End offset is before start offset"
        self._offsets = (ofs[0], ofs[1])

    @property
    def text(self):
        """
        Return string corresponding to the word, computed based
        on the offsets.
        """
        assert self.data is not None, \
            "Cannot compute text from None: {}.data is None".format(
                self.__class__.__name__)
        s, e = self.offsets
        return self.data[s:1+e]

    def __str__(self):
        return self.text
