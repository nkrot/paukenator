import sys
import pytest

from paukenator import Text

@pytest.fixture
def empty_text():
    return Text()

@pytest.fixture
def lines_1():
    return [
        "This is line 1",
        "# This is a comment",
        "This is line 2",
        "",
        "#END"
    ]

@pytest.fixture
def text_file_1(tmpdir, lines_1):
    # TODO: cleanup all intermediate directories as well. by default pytest keeps
    # three most recent runs
    fname = "text_file_1.txt"
    fileobj = tmpdir.join(fname)
    fileobj.write("\n".join(lines_1))
    yield str(fileobj)
    fileobj.remove(fname)

@pytest.fixture
def text_1(text_file_1):
    return Text.load(text_file_1)

def test_text_fields(empty_text):
    assert hasattr(empty_text, "lines")
    assert hasattr(empty_text, "lang")
    assert hasattr(empty_text, "skip_comments")

def test_text_defaults(empty_text):
    assert empty_text.lang == 'deu'
    assert empty_text.is_empty()
    assert empty_text.skip_comments == True

def test_text_load_from_file(text_file_1, lines_1):
    doc = Text.load(text_file_1)
    assert isinstance(doc, Text)
    assert doc.lines == lines_1

def test_new(lines_1):
    text = Text(lines_1)
    assert len(lines_1) == len(text.lines)
    assert not text.is_empty()

def test_is_comment(text_1):
    assert text_1.is_comment('#hello')
    assert not text_1.is_comment('hello # world')

def test_iterate_over_lines_including_comments(text_1, lines_1):
    text_1.skip_comments = False
    lines = [l for l in text_1]
    assert lines_1 == lines

def test_iterate_over_lines_skipping_comments(text_1, lines_1):
    text_1.skip_comments = True
    text_lines = [l for l in text_1]
    expected = [l for l in lines_1 if not text_1.is_comment(l)]
    assert expected == text_lines
    assert len(lines_1) > len(text_lines)

def test_word_counts(lines_2):
    text = Text()
    text.lines = list(lines_2)
    assert text.skip_comments
    assert 73 == len(text.wordcounts)
    assert 4 == text.wordcounts['is']
    assert 4 == text.wordcounts['the']
    assert 2 == text.wordcounts['The']
    assert 1 == text.wordcounts['horizon']
    assert 1 == text.wordcounts['horizon.']
    assert 0 == text.wordcounts['ways']
    assert 1 == text.wordcounts['ways,']
