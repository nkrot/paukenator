import sys
import pytest

from paukenator.text import Text

@pytest.fixture
def empty_text():
    return Text()

@pytest.fixture
def lines_1():
    return [ "This is line 1",
             "# This is a comment",
             "This is line 2",
             "",
             "#END"]

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

def test_text_defaults(empty_text):
    assert empty_text.lang == 'deu'
    assert empty_text.is_empty()
    assert empty_text.skip_comments == True

def test_text_load_from_file(text_file_1, lines_1):
    doc = Text.load(text_file_1)
    assert isinstance(doc, Text)
    assert doc.lines == lines_1

def test_iterate_over_lines_of_text(text_1, lines_1):
    text_1.skip_comments = False
    lines = []
    for line in text_1:
        lines.append(line)
    assert lines_1 == lines

def test_is_comment(text_1):
    assert text_1.is_comment('#hello')
    assert not text_1.is_comment('hello # world')

def test_iterate_over_lines_skipping_comments(text_1, lines_1):
    text_1.skip_comments = True
    lines = []
    for line in text_1:
        lines.append(line)
    lines_1_no_comments = [line for line in lines_1 if not text_1.is_comment(line)]
    assert lines_1_no_comments == lines
