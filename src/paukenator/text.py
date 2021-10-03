"""
Text as used in Lesson.
"""

import re
from paukenator import nlp
from typing import List


class Text(object):
    '''Text as used in a Lesson. Such a Text is assumed to be preprocessed
    for paragraphs, sentences and tokenized and is assumed to have:
    * one sentence per line
    * words separated by whitespaces.
    Therefore, no retokenization is attempted.

    A Text is a collection of Text.Sentence objects (not to be confused with
    nlp.Sentence annotatons).

    Internally, Text uses nlp.Text and provides functionality that is required
    in a Lesson.
    '''

    @classmethod
    def load_from_file(cls, fpath: str, config: 'Config'):
        '''Load content of given file <fpath> into Text object, assuming that
          - one line is one sentence
          - tokens are separated by whitespace (text already tokenized).
        '''
        pa = nlp.ParagraphAnnotator(lang=config.lang)
        sa = nlp.SentenceAnnotator(lang=config.lang)
        ta = nlp.TokenAnnotator(lang=config.lang)

        # assume text is already tokenized and avoid retokenizing
        sa.one_per_line = True
        ta.split_by_whitespace = True

        pipeline = [pa, ta, sa]

        text = nlp.Text.load_from_file(fpath, lang=config.lang)
        for annotator in pipeline:
            annotator(text)
        # print("--- Text loaded:\n{}\n----".format(text.tokenized()))

        obj = cls(text)
        obj.filename = fpath

        return obj

    def __init__(self, source: nlp.Text):
        self.source: nlp.Text = source
        self.filename: str = None
        self._sentences: List['Sentence'] = None

    @property
    def sentences(self) -> List['Sentence']:
        '''Return a list of sentences from the current text.'''
        if self._sentences is None:
            self._sentences = []
            for idx, sent in enumerate(self.source.sentences()):
                self._sentences.append(self.Sentence(sent, idx))
        return self._sentences

    def words_no_punctuations(self) -> List[str]:
        '''Return a uniqued list of words in the text excluding punctuation
        marks.'''
        def not_pm(wd):
            return not re.match(r'^[-,.;:?!{}\[\]()"\']+$', wd)
        # We cannot keep here nlp.Token because they cannot be uniqued,
        # therefore we convert them to strings.
        words = set(str(t) for t in self.source.tokens())
        words = list(filter(not_pm, words))
        return words

    class Sentence(object):
        '''Wrapper around nlp.Sentence that adds some fields'''

        def __init__(self, source: nlp.Sentence, num: int = -1):
            self.source: nlp.Sentence = source
            self.num: int = num

        @property
        def words(self) -> List[nlp.Token]:
            '''Return a list of all words of the sentence, unfiltered.'''
            return self.source.tokens()

        def __str__(self):
            # This will return the text as it was loaded from the file.
            # Alternatively, may want to generate output based on self.words
            return str(self.source)

