import pytest

from paukenator.nlp import Word


@pytest.fixture
def empty_word():
    wd = Word()
    return wd


@pytest.fixture
def sample_1_str():
    return "Hello, beautiful world!"


@pytest.fixture
def sample_1_data(sample_1_str):
    return [
        ("Hello",     (0, 4)),
        (",",         (5, 5)),
        ("beautiful", (7, 15)),
        ("world",     (17, 21)),
        ("!",         (22, 22))
    ]


@pytest.fixture
def sample_1_words(sample_1_data, sample_1_str):
    words = []
    for text, offsets in sample_1_data:
        wd = Word()
        wd.offsets = offsets
        wd.data = sample_1_str
        words.append(wd)
    return words


@pytest.fixture
def word(sample_1_words):
    return sample_1_words[0]


def test_fields(word):
    assert hasattr(word, "data")
    assert hasattr(word, "offsets")
    assert hasattr(word, "text")


def test_text(sample_1_data, sample_1_words):
    for wd, src in zip(sample_1_words, sample_1_data):
        assert len(wd.text) == len(src[0]), "Length do not match"
        assert wd.text == src[0], "Content (textual value) do not match"
        assert str(wd) == src[0], "Serialization to string does not match"


def test_get_text_from_empty_data(empty_word):
    empty_word.offsets = (0, 5)  # fake
    with pytest.raises(AssertionError):
        empty_word.text


@pytest.mark.parametrize(
    "offsets,descr", [
        ((1, ),       "not enough values"),
        ((0, 10, 30), "extra values"),
        ((10, 1),     "begin offset is past end offset"),
        ("ab",        "wrong type: a string looks like a tuple"),
        (20,          "wrong type")
    ])
def test_set_wrong_offsets(empty_word, offsets, descr):
    with pytest.raises(AssertionError):
        empty_word.offsets = offsets
