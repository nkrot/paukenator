import pytest

from paukenator import Text, TokenizedText


@pytest.fixture
def lines_2_as_words(lines_2_tokenized):
    return [ln.split() for ln in lines_2_tokenized]


@pytest.fixture
def text_2(lines_2, lines_2_as_words):
    tokenized_text = TokenizedText(Text(lines_2))
    tokenized_text.lines = lines_2_as_words
    return tokenized_text


def test_fields(text_2):
    assert hasattr(text_2, "original")


def test_new(text_2, lines_2_tokenized):
    assert isinstance(text_2, TokenizedText)
    assert text_2.skip_comments
    assert len(lines_2_tokenized) == len(text_2.lines)
    assert isinstance(text_2.original, Text)


def test_is_comment(text_2):
    assert text_2.is_comment(['#', 'hello'])
    assert not text_2.is_comment(['hello', '#', 'world'])


def test_iteration_gives_lists_of_words(text_2):
    text_2.skip_comments = False  # deliberately including comments
    for line in text_2:
        assert isinstance(line, list)


def test_iterate_over_lines_including_comments(text_2, lines_2_as_words):
    text_2.skip_comments = False
    text_lines = [ln for ln in text_2]
    assert len(lines_2_as_words) == len(text_lines)


def test_iterate_over_lines_skipping_comments(text_2, lines_2_as_words):
    text_2.skip_comments = True
    text_lines = [ln for ln in text_2]
    expected = [ln for ln in lines_2_as_words if not text_2.is_comment(ln)]
    assert expected == text_lines
    assert len(lines_2_as_words) > len(expected)  # sanity check


def test_word_counts(text_2):
    assert 70 == len(text_2.wordcounts)
    assert 4 == text_2.wordcounts['is']
    assert 4 == text_2.wordcounts['the']
    assert 2 == text_2.wordcounts['The']
    assert 2 == text_2.wordcounts['horizon']
    assert 0 == text_2.wordcounts['horizon.']
    assert 1 == text_2.wordcounts['ways']
    assert 0 == text_2.wordcounts['ways,']
