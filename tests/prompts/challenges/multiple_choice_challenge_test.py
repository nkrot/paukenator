import re
import pytest

from paukenator.prompts import InteractivePrompt
from paukenator.prompts.challenges import MultipleChoiceChallenge
from paukenator.text import Text


@pytest.fixture
def prompt(exercise, text_eng_1_lesson_text):
    # TODO: we do not want to know anything about Prompt when testing Challenge
    p = InteractivePrompt()
    p.text = text_eng_1_lesson_text
    p.challenge_class = MultipleChoiceChallenge
    p.exercise = exercise
    p.create_challenges()
    return p


@pytest.fixture
def challenges(prompt):
    return prompt.challenges


def test_create_choices(challenges, hidden_words):
    for ch, hw in zip(challenges, hidden_words):
        ch.create_choices()
        # print(ch)
        assert ch.num_choices == len(ch.choices), \
            "The number of choices should match the configured value"
        # print("Choice[0]", repr(ch.choices[0]))
        assert any(choice.value == hw.text for choice in ch.choices), \
            "Correct answer should be present among choices"
        exp_names = [str(i) for i in range(1, 1+ch.num_choices)]
        act_names = [choice.name for choice in ch.choices]
        assert exp_names == act_names, \
            "Choices should be named starting from 1"


def test_question(challenges, hidden_words):
    total = len(hidden_words)
    for idx, ch in enumerate(challenges):
        question = ch.question()
        num = 1+idx  # human-friendly enumeration
        exp = (rf'Question #{num} of {total}.'
                 ' To answer, please type in the number')
        assert re.search(exp, question)
        collected_choices = []
        for line in question.split('\n'):
            # TODO: string-form of a choice is defined in Choice class.
            # Does it make sense to use Choice class somehow here?
            if re.search(r' option \d', line):
                collected_choices.append(line)
        assert ch.num_choices == len(collected_choices), \
            "Wrong number of choices"
        for idx, line in enumerate(collected_choices):
            assert re.search(fr'option {1+idx}', line), \
                "Choices should be numbered starting from 1."
        correct = rf'option \d+: {ch.word.text}\b'
        assert any([re.search(correct, ln) for ln in collected_choices]), \
            "Correct option is not available among choices"


def test_correct_answer_is_provided(challenges, hidden_words):
    for ch, hw in zip(challenges, hidden_words):
        ch.create_choices()
        assert ch.answer is None, "Wrong default value"
        assert not ch.answered_correctly, "Wrong default value"
        # the answer in MultipleChoiceChallenge is the number of the option
        n = int(ch.correct_answer)
        assert n in range(1, 1+ch.num_choices)
        assert hw.text == ch.choices[n-1].value
