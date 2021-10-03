from typing import List, Type

from .annotator import Annotator
from .annotations import Text, Line
from .symbols import *


class LineAnnotator(Annotator):
    '''
    Annotate lines (between ^ and $) of text as Line. A Line is not
    a linguistic annotation.

    A Line is literally a line in the file.
    Annotation of lines should happen early, as it serves as a basis for
    other annotations.

    TODO:
    - distinguish comments
    '''

    @property
    def type(self) -> Type['Annotation']:
        '''Type of annotations produced by this class'''
        return Line

    def annotate(self, text: 'Text') -> None:
        '''Create annotations of type Line in given <text> in place.'''

        spans: List[T_SPAN] = []

        # Method splitlines() ignores the newline character \n just before EOF,
        # this is what we want.
        lines = text.source.content.splitlines()

        start, end = 0, 0
        for line in lines:
            end = start + len(line)
            spans.append((start, end))
            start = 1+end

        self.annotate_spans(text, spans)

