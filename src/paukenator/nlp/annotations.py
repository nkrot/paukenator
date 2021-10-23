from typing import List, Tuple, Optional
from .symbols import *
from .errors import NLPError


class AnnotationError(NLPError):
    '''Any error related to Annotation and subclasses'''


class TextData(object):
    '''Container for text data.
    All Annotations reference it and use it as a source of text data.
    '''
    # TODO: Why do I need this class? why cant it be Text with additional fields
    # hide this class inside Text and delegate some methods?

    @classmethod
    def load_from_file(cls, filepath):
        obj = cls()
        with open(filepath) as fd:
            obj.filepath = filepath
            obj.content = fd.read(-1)
        # print(f"---{obj.content}---")
        return obj

    def __init__(self):
        self.filepath: str = None
        self.content: str = None # text inself
        self.annotations: List[Annotation] = [] # or into Text?
        self.annotation_types = []
        self.root: Text = None  # top level annotation


class Annotation(object):
    '''
    Annotation is a base class for all other types more specific types of
    annotations. Ideally, one does not need to create an object of type
    Annotation directly.

    An annotation does not contain text data directly but by proxy of
    a TextData object.
    '''

    def __init__(self, span=(None, None)):
        assert len(span) == 2, \
          "A span (offsets) must contain 2 elements but got: {}".format(span)

        self.id = None
        self.start: int = span[0]
        self.end: int = span[1]
        #self.level = None
        self.language = None
        self._source: TextData = None

    def __repr__(self):
        return "<{}: id={}, offsets={}, text='{}'>".format(
            self.__class__.__name__, self.id, self.offsets, self.text)

    def __str__(self):
        return self.text

    def __len__(self):
        '''Length in bytes (not in characters)'''
        if self.end:
            return self.end - self.start
        return 0

    def is_blank(self):
        '''Test if the annotation is blank or not. A blank annotation has no
        text or consists of whitespace characters only.'''
        return len(self) == 0 or self.text.isspace()

    def __lt__(self, other):
        '''By offsets, from left to right'''
        # TODO: allow comparing different types of Annotations?
        # does it make sense?
        assert type(self) is type(other), \
            ("Can compare annotations of the same type only but got:"
             " {} and {}".format(type(self), type(other)))
        res = self.end <= other.start
        # print("Comparing: {} vs {} = {}".format(self.end, other.start, res))
        return res

    def __contains__(self, other):
        '''Test of other annotation is within boundaries of the current annotation'''
        return self.start <= other.start and self.end >= other.end

    @property
    def source(self):
        return self._source

    # TODO: what should happen when source gets set?
    @source.setter
    def source(self, obj: TextData):
        assert isinstance(obj, TextData), "Unsupported type of object"
        self._source = obj

    @property
    def offsets(self) -> T_SPAN:
        return (self.start, self.end)

    @property
    def text(self):
        # TODO: naming conflict: this name should be for the annotation Text?
        if self.source:
            return self.source.content[self.start:self.end]
        return None

    @property
    def root(self):
        if self.source:
            return self.source.root
        return None

    def add_annotation(self, ann: 'Annotation'):
        ann.reoffset(self.start)
        ann.source = self.source
        ann.source.annotations.append(ann)
        # register annotation type as added to the current object
        t = type(ann)
        if t not in ann.source.annotation_types:
            ann.source.annotation_types.append(t)

    def reoffset(self, val: int):
        '''Shift annotation position by given number of characters.'''
        self.start += val
        self.end += val

    def annotations(self, target=None):
        '''List *all* annotations or annotations of given type <target> that
        occur within the boundaries of the current annotation.
        Target can be a tuple of type names: (Token, WSWord)'''
        if target:
            anns = [ann for ann in self.source.annotations
                    if isinstance(ann, target)]
        else:
            anns = self.source.annotations
        anns = [ann for ann in anns if ann in self]
        return anns

    def paragraphs(self):
        '''Return a list of annotations of type Paragraph'''
        ann_type = Paragraph
        self._must_be_annotated(ann_type)
        return sorted(self.annotations(ann_type))

    def sentences(self):
        '''Return a list of annotations of type Sentence'''
        ann_type = Sentence
        self._must_be_annotated(ann_type)
        return sorted(self.annotations(ann_type))

    def lines(self):
        '''Return a list of annotations of type Line'''
        ann_type = Line
        self._must_be_annotated(ann_type)
        return sorted(self.annotations(ann_type))

    def wswords(self):
        '''Return a list of annotations of type WSWord'''
        ann_type = WSWord
        self._must_be_annotated(ann_type)
        return sorted(self.annotations(ann_type))

    def tokens(self):
        '''Return a list of annotations of type Token'''
        ann_type = Token
        self._must_be_annotated(ann_type)
        return sorted(self.annotations(ann_type))

    def next(self, scope: 'Annotation' = None):
        '''Get the next adjacent annotation of the same type.
        If <scope> is given (and is another annotation), also ensure that
        the annotation found is contained in the annotation <scope>.
        This is intended to be used for finding another annotation within
        the same super annotation, for example, finding next word that
        belongs to the same sentence.

        Example:
        >> word.next(word.line())
        '''
        scope = scope or self.root
        anns = sorted(scope.annotations(target=self.__class__))
        idx = anns.index(self)
        ann = None
        if idx is not None and 1+idx < len(anns):
            ann = anns[1+idx]
        return ann

    def line(self) -> Optional['Line']:
        '''Find annotation of type Line that contains current annotation'''
        anns = [line for line in self.root.lines() if self in line]
        assert len(anns) < 2, \
            ("ERROR: an annotation can be contained in one Line annotation"
            " only but found {} Lines".format(len(anns)))
        return anns[0] if anns else None

    def _must_be_annotated(self, anntype):
        '''Check if current object has been annotated for specific phenomena
        (e.g. Paragraphs, Sentences, Tokens, etc) and thrown an error if not.
        '''
        anntypes = self.source.annotation_types
        if anntype not in anntypes:
            raise AnnotationError(
                f"Annotations of type {anntype} not available in the current"
                " object. Was appropriate annotator applied to the text?"
            )

    def tokenized(self):
        '''Return the current annotation as a single tokenized line.'''
        return " ".join(map(str, self.tokens()))


class Text(Annotation):
    '''Annotation that represents the whole text'''

    @classmethod
    def load_from_file(cls, filepath: str, **kwargs):
        '''Load plain text from given file <filepath> and annotate it for
        - lines (annotation.Line)
        - words (annotation.WSWord, separated by white spaces)

        Return:
        annotation.Text
        '''
        textdata = TextData.load_from_file(filepath)

        # print("--- Text annotation ---")
        text = cls()
        text.source = textdata
        text.language = kwargs.get('lang', 'deu')

        # print(text.offsets)
        # print(repr(text))

        textdata.root = text

        # print("--- Annotating Lines ---")
        LineAnnotator().annotate(text)
        # for ann in text.lines():
        #     print(repr(ann))

        # print("--- Annotating WSWords ---")
        WSWordAnnotator().annotate(text)
        # for ann in text.wswords():
        #     print(repr(ann))

        return text

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, obj: TextData):
        '''Set source and create annotation of class Text'''
        self._source = obj
        self.start = 0
        self.end = len(self.source.content)

    def tokenized(self):
        '''Serialize the current object to a string. The text is fully
        tokenized, that is:
          - one sentence per line;
          - paragraphs are separated by an empty line;
          - words are separated from punctuation marks
        '''
        lines = []
        for par in self.paragraphs():
            for sent in par.sentences():
                words = sent.tokens()
                # words = sent.wswords()
                line = " ".join(map(str, words))
                lines.append(line)
            lines.append('')  # paragraph separator
        if lines:
            lines.pop()
        return "\n".join(lines)


class Line(Annotation):
    '''Annotation that holds one line of a Text'''
    pass


class Paragraph(Annotation):
    pass


class Sentence(Annotation):
    '''Annotation that holds a sentence.'''
    pass


class WSWord(Annotation):
    '''A substring of text between two space characters.
    It can be a word, a punctuation mark or combination of them.
    Not to be confused with a Token.

    WSWord stands for WhiteSpace Word.
    '''
    pass


class Token(Annotation):
    '''A Token is either a lexeme (stripped off punctuation marks) or
    a punctuation mark.'''
    pass


# These are necessary in Text.load_from_file() and are imported here at
# the end of the file to fix circular dependencies.
from .line_annotator import LineAnnotator
from .wsword_annotator import WSWordAnnotator
