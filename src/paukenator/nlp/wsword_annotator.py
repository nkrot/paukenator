import re
from typing import List, Type

from .annotator import Annotator
from .annotations import Text, WSWord
from .symbols import *


class WSWordAnnotator(Annotator):
    '''Annotates words in text with as annotations of type WSWord.
    A word for this annotator is a substrign of text surrounded by whitespace
    characters or beginning/end of line.

    WSWord is not a linguistic annotation and should not be confused with
    Token annotation.
    '''

    @property
    def type(self) -> Type['Annotation']:
        '''Type of annotations produced by this annotator.'''
        return WSWord

    def annotate(self, text: Text) -> None:
        spans: List[T_SPAN] = []
        for m in re.finditer(r'\S+', text.source.content):
            spans.append(m.span())
        self.annotate_spans(text, spans)
