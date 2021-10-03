"""tests for paragraph annotator"""

import pytest
from paukenator.nlp import ParagraphAnnotator, Paragraph


def test_has_property_type():
    assert hasattr(ParagraphAnnotator, "type"), \
        ("ParagraphAnnotator must have a property `type` that returns the type"
         " of created annotations.")
    exp, actual = Paragraph, ParagraphAnnotator().type
    assert exp == actual, \
        (f"ParagraphAnnotator is expected to produce objects of type {exp} but"
         f" got {actual}")


def test_raise_error_if_not_annotated(text_deu_1):
    '''An attempt to request text.paragraphs() should result an error if
    the text is not annotated for Paragraphs'''
    with pytest.raises(RuntimeError):
        text_deu_1.paragraphs()


def test_1(text_deu_1):
    '''This is the simplest case of text for which paragraph annotator should
    work reliably and stably:
    - a paragraph is exactly one line of text;
    - paragraphs are separated by exactly one empty line;
    - an empty line is really empty, no blank characters.
    '''
    text = text_deu_1
    ParagraphAnnotator()(text)
    exp, actual = 3, len(text.paragraphs())
    msg = "Number of paragraphs in {} does not match, expected {} but got {}"
    assert exp == actual, msg.format(text.source.filepath, exp, actual)


def test_empty_lines_separate_paragraphs(text_deu_2):
    '''One paragraph is one or several lines separated by one or more empty
    or blank lines.
    '''
    text = text_deu_2
    ParagraphAnnotator()(text)
    paragraphs = text.paragraphs()

    exp, actual = 4, len(paragraphs)
    msg = "Number of paragraphs in {} does not match, expected {} but got {}."
    assert exp == actual, msg.format(text.source.filepath, exp, actual)

    exp = [2, 1, 5, 3]
    actual = [len(par.lines()) for par in paragraphs]
    msg = ("Number of lines in paragraphs in {} does not match, expected {}"
           " but got {}.")
    assert exp == actual, msg.format(text.source.filepath, exp, actual)
