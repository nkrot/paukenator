import pytest

from paukenator.nlp import SBD, Sentence
from paukenator.text import Text


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
def sbd1():
    sbd = SBD()
    return sbd


@pytest.fixture
def text_1(lines_1):
    t = Text()
    t.lines = lines_1
    return t


def test_fields(sbd1):
    assert hasattr(sbd1, "lang")


def test_process_string(sbd1):
    text = "Hello, amazing world!"
    sents = sbd1.process(text)
    assert isinstance(sents, list), \
        "Method should return a list and not a single item"
    types = [type(s) for s in sents]
    assert all(isinstance(s, Sentence) for s in sents), \
        f"Expecting list of Sentence but got: {types}"


@pytest.mark.parametrize("obj", [
    1,
    ("aa", 2),
    ["l1", "l2"]
])
def test_process_errors_on_non_string(sbd1, obj):
    with pytest.raises(AssertionError):
        sbd1.process(obj)


@pytest.mark.parametrize("obj", [
    1,
    "hello world",
    ("aa", 2),
    ["l1", "l2"]
])
def test_annotate_errors_on_nontext(sbd1, obj):
    with pytest.raises(AssertionError):
        assert sbd1.annotate(obj)


def test_annotate_accepts_text(sbd1, text_1):
    assert len(text_1.sentences) == 0
    sbd1.annotate(text_1)
    assert len(text_1.sentences) > 0, \
        "SBD did not annotate sentences in Text"
    assert len(text_1.sentences) == 2, \
        "SBD annotated more or less sentences in Text"
    linums = [s.linum for s in text_1.sentences]
    assert [0, 2] == linums, "Sentence objects have wrong <linum> attribute"
