
class Sentence(object):

    def __init__(self):
        # object being annotated
        self.data = None  # str
        # character offset of the span in self.data that corresponds
        # to the current sentence
        self._offsets = None  # (start, end) 0-based
        self._words = None    # list of words as str or Word objects

    def __iter__(self):
        return iter(self.words)

    @property
    def words(self):
        return (self._words or [])

    @words.setter
    def words(self, wds):
        self._words = wds

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
        Return string corresponding to the sentence, computed based
        on the offsets.
        """
        assert self.data is not None, \
            "Cannot compute text from None: {}.data is None".format(
                self.__class__.__name__)
        s, e = self.offsets
        return self.data[s:1+e]

    def __str__(self):
        return self.text
