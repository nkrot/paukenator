# TODO: try using standard re instead of regex.
import regex as re
#import re
from typing import List, Type

from .annotator import Annotator
from .annotations import Text, Sentence
from .symbols import *


class SentenceAnnotator(Annotator):
    '''Create annotations of type Sentence in a text.

    Sentences are linguistic entities. Annotation of Sentences requires
    language-specific knowledge and uses semantic dictionary.

    Sentence annotator expects Lines to be available in the text.
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.one_per_line = False

    @property
    def type(self) -> Type['Annotation']:
        '''Type of annotations produced by this annotator.'''
        return Sentence

    def _find_sentences(self, text: str) -> List[T_SPAN]:
        '''Find positions where sentences start and end in given string.'''
        spans = []

        # TODO: move it to shared resources
        ROMAN = '(II?I?|I?V|VII?I?|I?X)'  # some of roman numbers

        # beginning of line
        # TODO: use line.start (careful: it is relative to Text)
        spans.append([0]) # assume text starts at the beginning of Line.

        # BUG: this can not detect overlapping matching and does not catch
        # the case (in text.02.txt): ... z.B. Brombeeren . Das Ganze ...
        reg = r'(?P<head>\S*)(?P<pm>[.!?][)]?)\s+(?P<tail>\S*)'

        for m in re.finditer(reg, text):
            # self.dprint(m)

            # TODO: name parts meaningfully? otherwise hard to support
            parts = {n: (v, m.span(n)) for n, v in m.groupdict().items()
                     if v is not None}
            # self.dprint(parts)
            # print(parts)

            do_split = False
            if parts['pm'][0] in {'?', '!'}:
                # split unconditionally by ? or !
                do_split = True

            elif re.match(r'[(\"]?[[:upper:]][[:lower:]]', parts['tail'][0]):
                do_split = True

                wd = parts['head'][0] + parts['pm'][0]
                if wd in self.semdict('NO_SENT_END'):
                    # z.B. Brombeeren
                    do_split = False

                # TODO: getting next word WITHOUT punctuation would allow for
                # a more reliable checking in the dictionaries
                nxw = parts['tail'][0]

                if (re.match(r'[0-3]?[0-9]\.$', self.lstrip(wd))
                    and self.rstrip(nxw) in self.semdict('MONTH_NAMES')):
                    # am 25. Oktober
                    do_split = False

                if (re.match(rf'(\d\d?|{ROMAN})\.$', self.lstrip(wd))
                    and self.rstrip(nxw) in self.semdict('NOUNS_WITH_ORDINAL_NUMBER')):
                    # more generally, a noun preceeded by an ordinal numeral
                    # ex: im 10. Jahrhundert
                    do_split = False

            elif re.match(r'[12]?\d\d\d$', parts['tail'][0]):
                # next sentence starts with a year:
                # ex: ... belegt. 1106 wurde in Italien ...
                do_split = True

            if do_split:
                e = parts['pm'][1][-1]   # end of punctuation
                s = parts['tail'][1][0]  # start of the next word
                spans[-1].append(e)
                spans.append([s])

        # end of line is always end of sentence
        spans[-1].append(len(text))

        return spans

    def lstrip(self, s: str):
        '''Remove all punctuation marks from the left side of the string <s>'''
        # TODO: extend regexp
        s = re.sub(r'^[-"({[]+', '', s)
        return s

    def rstrip(self, s: str):
        '''Remove all punctuation marks from the right side of the string <s>'''
        # TODO: extend regexp
        s = re.sub(r'[]})",.!?-]+$', '', s)
        return s

    def _find_sentences_one_per_line(self, line: str) -> List[T_SPAN]:
        '''A line is itself a sentence.'''
        # Could otherwise just copy offsets from given Line but the offsets
        # are absolute in this case and annotate_spans() will not be suitable.
        return [(0, len(line))]

    def annotate(self, text: Text) -> None:
        '''Annotate sentences in given <text> in place, creating annotations
        of type Sentence.
        For now, assume that a Sentence never spans more that one line.

        TODO
        - ignore lines that are comments
        - walk paragraphs or Text? if walking the Text, how to ignore lines that
        are comments that can appear nested?
        '''

        for line in text.lines():
            if not line.is_blank():
                if self.one_per_line:
                    spans = self._find_sentences_one_per_line(line.text)
                else:
                    spans = self._find_sentences(line.text)
                self.dprint(spans)
                self.annotate_spans(line, spans)

