"""
Collection of NLP (Natural Language Processing) tools for analysing a text.

This module provides a set of tools to perform analysis of text, namely
recognition of paragraphs, sentences and tokens (words and punctuation marks).
The results of analysis are created in form of Annotations. An Annotation marks
a substring of a text (identified by offsets) as being of certain type, for
example a Sentence, a Token, etc. A client can then access individual sentences,
tokens or other annotations.

An Annotation of a specific type is typically created by a dedicated Annotator.

Annotations
-----------
1. Text   [created when file is loaded] represents the whole text.
2. Line   [by LineAnnotator] represents a single line from a text.
3. WSWord [by WSWordAnnotator] represents a single word, that is understood as
           a sequence of characters between two white space characters.

The following annotations are linguistic phenomena, recognition of which may
require language-specific knowledge. Some of such knowledge is provided in
so called Semantic Dictionary (see `semdict.SemDict`). The annotators load
an appropriate semantic dictionary automatically.
4. Paragraph [by ParagraphAnnotator]
5. Sentence  [by SentenceAnnotator]
6. Token     [by TokenAnnotator]

For more information, please refer to corresponding Annotation or Annotator
subclasses.

USAGE
-----
Load the text from a file.
This will automatically annotate Lines and WSWords
>>> atext: Text = nlp.Text.load_from_file("path/to/file.txt", lang='deu')

For annotating other phenomena, corresponding annotators need to be run
explicitly. First, create annotators:
>>> pa = ParagraphAnnotator(lang='deu')
>>> sa = SentenceAnnotator(lang='deu')
>>> ta = TokenAnnotator(lang='deu')

then apply them:
>>> pa(atext)
>>> sa(atext)
>>> ta(atext)
"""

#from .errors import *
from .symbols import *
from .resources import *
from .semdict import SemDict  # , SemDictClassNotFoundError

from .annotations import TextData, Annotation, Text, Line, \
                         Paragraph, Sentence, WSWord, Token, \
                         AnnotationError

from .annotator import Annotator
from .paragraph_annotator import ParagraphAnnotator
from .line_annotator import LineAnnotator
from .sentence_annotator import SentenceAnnotator
from .wsword_annotator import WSWordAnnotator
from .token_annotator import TokenAnnotator


__all__ = [
    'TextData',
    'Annotation',  # base class, intended for internal use only
    'Text',
    'Line',
    'Paragraph',
    'Sentence',
    'WSWord',
    'Token',
    'AnnotationError',

    'Annotator',  # base class, intended for internal use only
    'ParagraphAnnotator',
    'LineAnnotator',
    'SentenceAnnotator',
    'WSWordAnnotator',
    'TokenAnnotator'
]

LANGUAGES = (
    ('deu', 'de', 'German'),
    ('eng', 'en', 'English')
)

DEFAULT_LANGUAGE = 'deu'
