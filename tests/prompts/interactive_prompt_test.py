"""
Tests for InteractivePrompt
"""

import re
import pytest

from paukenator.prompts import InteractivePrompt


@pytest.fixture(scope='function')
def prompt(hidden_words):
    p = InteractivePrompt()
    p.hidden_words = hidden_words
    return p


def test_fields(prompt):
    assert hasattr(prompt, "user_input")
    assert hasattr(prompt, "hidden_words")
    assert hasattr(prompt, "counts")
    assert hasattr(prompt, "max_attempts")
    assert 2 == prompt.max_attempts


def test_commands(prompt):
    assert sorted(['q', 'r', 's', 'S']) == sorted(prompt.COMMANDS.keys())


def test_help_message(prompt):
    msg = prompt.help_message()
    assert re.match('HELP:', msg)
    msg_words = msg.split()
    for cmd in prompt.COMMANDS.keys():
        assert cmd in msg_words, f"Key/command '{cmd}' in not in help message"
    assert hasattr(prompt, "show_help")


def test_hidden_words_given(monkeypatch):
    prompt = InteractivePrompt()
    monkeypatch.setattr('builtins.input', lambda _ : 'any')
    with pytest.raises(ValueError):
        prompt.run()


@pytest.mark.skip(reason="TODO: to test or not to test inherited method?")
def test_command_q(prompt):
    assert False


@pytest.mark.skip(reason="TODO: to test or not to test inherited method?")
def test_command_r(prompt):
    assert False


def test_command_s(prompt, mocker):
    mocker.patch('builtins.input', side_effect=['Hello', 's', 'amazing'])
    # state before
    assert prompt.user_input is None
    assert not prompt.skip_word
    assert not prompt.skip_sentence
    assert 0 == prompt.counts['answered']
    assert 0 == prompt.counts['skipped']
    # interact with user
    # NOTE: for the time being, this will make as many reads as there are
    # hidden_words.
    prompt.run()
    # state after
    assert prompt.user_input == 's'
    assert prompt.skip_word
    assert not prompt.skip_sentence
    assert 2 == prompt.counts['answered']
    assert 1 == prompt.counts['skipped']


def test_command_S(prompt, mocker):
    mocker.patch('builtins.input', side_effect=['Hello', 'S'])
    assert prompt.user_input is None
    assert not prompt.skip_word
    assert not prompt.skip_sentence
    # interact with user
    prompt.run()
    # state after
    assert prompt.user_input == 'S'
    assert not prompt.skip_word
    assert prompt.skip_sentence
    assert 1 == prompt.counts['answered']
    assert 2 == prompt.counts['skipped']


def test_user_answers_all_correctly(prompt, mocker, hidden_words):
    answers = [hw.text for hw in hidden_words]
    mocker.patch('builtins.input', side_effect=answers)
    prompt.run()
    assert prompt.counts['answered']  == len(answers)
    assert prompt.counts['skipped']   == 0
    assert prompt.counts['correct']   == len(answers)
    assert prompt.counts['incorrect'] == 0


def test_user_answers_all_incorrectly(prompt, mocker, hidden_words):
    wrong_answers = [hw.text[::-1].upper() for hw in hidden_words] \
                      * prompt.max_attempts
    mocker.patch('builtins.input', side_effect=wrong_answers)
    prompt.run()
    assert prompt.counts['answered']  == len(hidden_words)
    assert prompt.counts['skipped']   == 0
    assert prompt.counts['correct']   == 0
    assert prompt.counts['incorrect'] == len(hidden_words)


@pytest.mark.skip(reason='TODO')
def test_created_challenges():
    assert False

# TODO
# 1. test scenarios:
#    [(wrong, correct), S]
#    [(correct), S]
#    [(wrong, correct), s, (correct)]
# 2. test longer scenarios that span more than one sentence
