"""
"""
from collections import Counter


class Text(object):

    @classmethod
    def load(cls, fname, **kwargs):
        with open(fname) as fd:
            lines = fd.read().split('\n')
            # we normalize whitespace, otherwise WBD may produce inconsistent
            # tokenization. TODO: this should be fixed in WBD
            lines = [" ".join(ln.split()) for ln in lines]
            text = cls(lines)
            text.lang = kwargs.get('lang', 'deu')
            text.filename = fname
            return text

    @classmethod
    def is_comment(cls, line):
        return line.startswith('#') or line.startswith('::')

    def __init__(self, lines=None):
        self.lines = lines or []
        self.lang = 'deu'
        self.filename = None
        self.skip_comments = True
        self._wordcounts = None
        self.sentences = []

    # def __iter__(self):
    #     return self.LinesIterator(self)

    def is_empty(self):
        return len(self.lines) == 0

    def add_sentence(self, sent, linum):
        """Add sentence that comes from the line at position <linum>"""
        s = self.TextSentence(sent, linum, len(self.sentences))
        self.sentences.append(s)

    @property
    def sentences_available(self):
        """Tells whether SBD was applied"""
        not_applied = len(self.sentences) == 0 and len(self.lines) > 0
        return not(not_applied)

    @property
    def wordcounts(self):
        if self._wordcounts is None:
            if not self.sentences_available:
                # NOTE: strictly speaking, words can easily be counted w/o
                # knowing sentence boundaries.
                raise ValueError("Text must be split into sentences")
            self._wordcounts = Counter()
            for sent in self.sentences:
                words = [str(wd) for wd in sent.words]
                self._wordcounts.update(words)
        return self._wordcounts

    class TextSentence(object):
        """
        Wrapper for other types of Sentences that adds additional fields
        relevant to the Sentence as part of Text meanwhile delegating other
        methods to the underlying Sentence object.

        TODO: will it work for paragraphs as well?
        TODO: how to make this class identify itself as Sentence? is it needed?
        """

        def __init__(self, sent, linum=-1, num=-1):
            self.sent = sent
            self.linum = linum
            self.num = num  # position of the sentence among text sentences

        def __getattr__(self, name):
            attr = getattr(self.sent, name)
            if not callable(attr):
                return attr

            # TODO: what is this?
            def wrapper(*args, **kwargs):
                return attr(*args, **kwargs)
            return wrapper

        def __setattr__(self, name, value):
            # TODO: how to accomplish the same in a more general way?
            # namely, degelate any method to self.sent if it is not available
            # in self (like method_missing)?
            if name in ['words']:
                setattr(self.sent, name, value)
            else:
                # TODO: using super will create a new attribute. this is
                # undesired. Wht is Python such a shit?!
                super(self.__class__, self).__setattr__(name, value)

        def __iter__(self):
            return iter(self.sent)

        def __str__(self):
            return str(self.sent)

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
            self._items = [(idx, item) for idx, item in enumerate(lst)
                                       if self._is_valid(item)]

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
            return (not self.text.skip_comments
                    or not self.text.is_comment(line))
