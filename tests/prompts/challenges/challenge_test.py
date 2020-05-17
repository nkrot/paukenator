import pytest

from paukenator.prompts import InteractivePrompt
from paukenator.prompts.challenges import Challenge

# TODO
# 1. here challenges are created using InteractivePrompt, this does not look
#    good and should be redesigned.
# 2. test what is printed in analyse_answer()
# 3. test S (skip sentence) is processed
# 4. test q (quit) is processed


@pytest.fixture
def prompt(hidden_words):
    # TODO: we do not want to know anything about Prompt when testing Challenge
    p = InteractivePrompt()
    p.challenge_class = Challenge
    p.hidden_words = hidden_words
    p.create_challenges()
    return p


@pytest.fixture
def challenges(prompt):
    return prompt.challenges


def test_defaults(hidden_words):
    hw = hidden_words[0]
    challenge = Challenge(hw)
    assert 1 == challenge.max_attempts
    assert (1, 1) == challenge.info
    assert hw == challenge.word


def test_question(challenges, hidden_words):
    # NOTE: here we need to have a collection of challenges to test the text
    # if the question, and need to use Prompt.create_challenges(). Any better
    # way of designing the object space? Perhaps additional class ChallengeSet
    # would help?
    total = len(hidden_words)
    for idx, ch in enumerate(challenges):
        num = 1+idx  # human-friendly enumeration
        msg = (f'Question #{num} of {total}.'
                ' To answer, please type in a suitable word.')
        assert msg == ch.question()


def test_correct_answer_is_provided(challenges, hidden_words):
    for ch, hw in zip(challenges, hidden_words):
        assert ch.correct_answer == hw.text
        assert ch.answer is None, "Wrong default value"
        assert not ch.answered_correctly, "Wrong default value"


def test_very_smart_user(mocker, challenges):
    for ch in challenges:
        answer = ch.correct_answer
        # very smart gives correct answer immediately
        mocker.patch('builtins.input', side_effect=[answer])
        assert not ch.finished
        ch.make_attempt()
        assert 1 == ch.current_attempt
        assert ch.answered_correctly
        assert answer == ch.answer
        assert answer == ch.correct_answer
        assert ch.finished


def test_dumb_user(mocker, challenges):
    ch = challenges[0]
    ch.max_attempts = 3
    # a dump user never answers correctly
    mocker.patch('builtins.input', side_effect=['_', '_', '_'])
    # attempt #1
    assert not ch.finished
    ch.make_attempt()
    assert 1 == ch.current_attempt
    assert not ch.answered_correctly
    assert not ch.finished
    # attempt #2
    ch.make_attempt()
    assert 2 == ch.current_attempt
    assert not ch.answered_correctly
    assert not ch.finished
    # attempt #3
    ch.make_attempt()
    assert 3 == ch.current_attempt
    assert not ch.answered_correctly
    assert ch.finished


def test_decent_user(mocker, challenges):
    ch = challenges[0]
    ch.max_attempts = 3
    # decent user succeeds at the 2nd attempt
    mocker.patch('builtins.input', side_effect=['_', ch.correct_answer])
    # attempt #1
    assert not ch.finished
    ch.make_attempt()
    assert 1 == ch.current_attempt
    assert not ch.answered_correctly
    assert not ch.finished
    # attempt #2
    ch.make_attempt()
    assert 2 == ch.current_attempt
    assert ch.answered_correctly
    assert ch.finished


def test_challenge_was_skipped(mocker, challenges):
    ch = challenges[0]
    ch.max_attempts = 3
    mocker.patch('builtins.input', side_effect=['s'])
    ch.make_attempt()
    assert not ch.answered_correctly
    assert ch.finished
