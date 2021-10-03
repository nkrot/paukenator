from typing import List

from .annotator import Annotator
from .annotations import Text, Paragraph
from .symbols import *


class ParagraphAnnotator(Annotator):
    '''Recognize paragraphs in text and annotate them as Annotations of type
    Paragraph. Paragraphs are linguistic entities.

    A Paragraph is one or several lines, separated from other paragrapgs by
    one or more empty/blank lines. A paragraph therefore cannot have empty or
    blank lines in it.

    Annotation of Paragraphs requires Line annotations already being available.
    '''

    @property
    def type(self):
        '''The type of annotations that this annotator creates'''
        return Paragraph

    def annotate(self, text: Text):
        '''Create annotations of type Paragraph in <te1xt> modifying the latter
        in place.
        '''

        spans: List[int] = [[]] # stores start and end offsets

        for line in text.lines():
            # self.dprint(repr(line))

            if line.is_blank():
                spans.append([])
            else:
                spans[-1].extend(line.offsets)

        # take beginning of the 1st sentence and the end of the last sentence
        spans = [(span[0], span[-1]) for span in spans if span]

        self.annotate_spans(text, spans)


