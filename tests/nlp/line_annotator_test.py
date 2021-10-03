"""
Tests for LineAnnotator.
"""

from paukenator.nlp import LineAnnotator, Line


def test_text_deu_1_has_correct_number_of_lines(text_deu_1):
    exp, actual = 8, len(text_deu_1.lines())
    assert exp == actual, \
        f"Text must contain {exp} lines but got {actual}"


def test_has_property_type():
    assert hasattr(LineAnnotator, "type"), \
        ("LineAnnotator must have a property `type` that returns the type of"
         " created annotations.")
    exp, actual = Line, LineAnnotator().type
    assert exp == actual, \
        (f"LineAnnotator is expected to produce objects of type {exp} but"
         f" got {actual}")


def test_recognize_blank_non_empty_lines(text_deu_2):
    '''Check if we can tell apart blank and non-blank lines.
    A blank line is either an empty line, or a line with whitespace chars only.
    '''
    lines = text_deu_2.lines()

    idx = 7
    empty = lines[idx]
    actual = len(empty)
    assert 0 == actual, \
        f"Expecting the line at linum {idx} be zero size but got {actual}"
    assert empty.is_blank(), \
        f"Expecting the line at linum {idx} be identified as blank."

    idx = 13
    blank = lines[idx]
    actual = len(blank)
    assert 0 < actual, \
        f"Expecting the line at linum {idx} be non-zero size but got {actual}"
    assert blank.is_blank(), \
        f"Expecting the line at linum {idx} be identified as blank."

    # check against false positives
    idx = 12
    nonblank = lines[idx]
    actual = len(nonblank)
    assert 0 < actual, \
        f"Expecting the line at linum {idx} be non-zero size but got {actual}"
    assert not nonblank.is_blank(), \
        f"Expecting the line at linum {idx} be identified as non-blank."
