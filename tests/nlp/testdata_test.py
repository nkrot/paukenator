"""
Tests to validate the files used in testing.
The tests check whether necessary phenomena are still here, as it happens
sometimes that mere opening and closing a file modifies its content.
"""

import re


def test_text_deu_2_has_blank_lines(text_deu_2_lines):
    '''Check that there is a blank line in the text. A blank line is a line
    that consists entirely of space or tab characters.
    '''
    lines = text_deu_2_lines
    linum = 13
    msg = ("Line at linum {} is expected to be composed entirely of spaces"
           " or tabs but is not.")
    assert re.match(r'[ \t]+\n$', lines[linum]), msg.format(linum)


def test_text_deu_2(text_deu_2_lines):
    lines = text_deu_2_lines
    exp_first_chars = ['\n',
                       'A', 'W',
                       '\n',
                       'D',
                       '\n', '\n', '\n',
                       'W', 'E', 'D', 'D', 'D',
                       ' ',  # 13
                       'S', 'S', 'L',
                       '\n', '\n']
    actual_first_chars = [line[0] for line in lines]
    assert exp_first_chars == actual_first_chars, "Wrong line initials"
