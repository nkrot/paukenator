
import pytest
from paukenator.nlp import Text, Line, WSWord
from paukenator.nlp import AnnotationError


def test_file_is_as_expected(text_deu_1_lines):
    '''Check that the file against with we are testing has not changed.
    If this is the case, all subsequent test must hold as well.
    '''
    lines = text_deu_1_lines
    assert 8 == len(lines), f"File must have 8 lines but got: {len(lines)}"

    # the 1st character from every line
    exp_initials = ['#', '#', 'A', '\n', 'W', '\n', 'S', '#']
    initials = [line[0] for line in lines]
    fails = []
    for idx, pair in enumerate(zip(exp_initials, initials)):
        if pair[0] != pair[1]:
            fails.append((idx, pair))
    msg = "Mismatching 1st character in the {} lines: {}"
    assert exp_initials == initials, msg.format(len(fails), fails)


def test_text_is_loaded_from_file(text_deu_1):
    '''Text content of a file can be loaded directly from the file into
    an object of type nlp.Text.
    '''
    text = text_deu_1
    assert isinstance(text, Text), \
        "Expecting type pbject of type Text but got {type(text)}"

    exp = 2177  # bytes counted with `wc -m`
    msg = "Byte length mismatch, expected {} but got {}."
    assert exp == len(text), msg.format(exp, len(text))


def test_text_is_preannotated_for_lines(text_deu_1):
    '''When Text is created, it is automatically preannotated for Lines.'''
    lines = text_deu_1.lines()
    fails = []
    for idx, item in enumerate(lines):
        if not isinstance(item, Line):
            fails.append((idx, type(item), item))
    msg = "Expecting all lines to be of type Line but got {} cases: {}"
    assert not fails, msg.format(len(fails), fails)


def test_text_is_preannotated_for_wswords(text_deu_1):
    '''When Text is created, it is automatically preannotated for WSWords
    (whitespace separated words).
    '''
    wswords = text_deu_1.wswords()
    fails = []
    for idx, item in enumerate(wswords):
        if not isinstance(item, WSWord):
            fails.append((idx, type(item), item))
    msg = "Expecting all words to be of type WSWord but got {} cases: {}"
    assert not fails, msg.format(len(fails), fails)


def test_text_is_not_preannotated(text_deu_1):
    '''When Text is loaded, annotation of the following is not performed
    automatically:
     - no paragraphs
     - no sentences
     - no tokens
    '''
    text = text_deu_1
    with pytest.raises(AnnotationError):
        text.paragraphs()
    with pytest.raises(AnnotationError):
        text.sentences()
    with pytest.raises(AnnotationError):
        text.tokens()
