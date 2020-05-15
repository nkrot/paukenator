import pytest

from paukenator.nlp import Sentence


@pytest.fixture
def empty_sent():
    s = Sentence()
    return s


@pytest.fixture
def lines():
    return [
        ("Hello, beautiful world!", (0, 22)),
        # a space will be added between sentences
        ("How are you today",       (24, 42))
    ]


@pytest.fixture
def sentences(lines):
    text = " ".join([ln[0] for ln in lines])
    sents = []
    for ln in lines:
        s = Sentence()
        s.data = text
        s.offsets = ln[1]
        sents.append(s)
    return sents


@pytest.fixture
def sent(sentences):
    return sentences[0]


@pytest.fixture
def sent_with_words(sent):
    sent.words = sent.data.split()
    return sent


def test_fields(sent):
    assert hasattr(sent, "data")
    assert hasattr(sent, "offsets")
    assert hasattr(sent, "text")
    assert hasattr(sent, "words")


def test_text(sentences, lines):
    for s, ln in zip(sentences, lines):
        assert len(ln[0]) == len(s.text), "Lengths do not match"
        assert ln[0] == s.text, "Textual values do not match"


def test_get_text_from_empty_data(empty_sent):
    empty_sent.offsets = (0, 10)  # fake
    with pytest.raises(AssertionError):
        empty_sent.text


@pytest.mark.parametrize(
    "offsets,descr", [
        ((1, ),       "not enough values"),
        ((0, 10, 30), "extra values"),
        ((10, 1),     "begin offset is past end offset"),
        ("ab",        "wrong type: a string looks like a tuple"),
        (20,          "wrong type")
    ])
def test_set_wrong_offsets(empty_sent, offsets, descr):
    with pytest.raises(AssertionError):
        empty_sent.offsets = offsets


def test_iterate_over_words(sent_with_words):
    exp_words = sent_with_words.data.split()
    act_words = [wd for wd in sent_with_words]
    assert len(exp_words) == len(act_words), "Number of words does not match"
    # assert exp_words == act_words, "Listing of words does not match"
