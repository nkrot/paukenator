"""
Tests for SimplePrompt
"""

import re
import pytest

from paukenator.prompts import SimplePrompt


@pytest.fixture
def prompt():
    return SimplePrompt()


def test_fields(prompt):
    assert hasattr(prompt, "user_input")
    assert hasattr(prompt, "counts")
    assert hasattr(prompt, "text")
    assert not prompt.is_interactive


def test_commands(prompt):
    assert ['q', 'r'] == sorted(prompt.COMMANDS.keys())


def test_help_message(prompt):
    msg = prompt.help_message()
    assert re.match('HELP:', msg)

    msg_words = msg.split()
    for cmd in prompt.COMMANDS.keys():
        assert cmd in msg_words, f"Key/command '{cmd}' in not in help message"

    assert hasattr(prompt, "show_help")


def test_command_q(prompt, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'q')
    # state before
    assert prompt.user_input is None
    assert prompt.is_running
    assert prompt.proceed
    prompt.run()
    # state after
    assert prompt.user_input == 'q'
    assert not prompt.is_running
    assert prompt.proceed  # TODO: this is strange


def test_command_r(prompt, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'r')
    # state before
    assert prompt.user_input is None
    assert prompt.is_running
    assert prompt.proceed
    prompt.run()
    # state after
    assert prompt.user_input == 'r'
    assert prompt.is_running
    assert not prompt.proceed


def test_command_another(prompt, monkeypatch):
    # initial state
    assert prompt.is_running
    # first interaction
    monkeypatch.setattr('builtins.input', lambda _: 'n')
    prompt.run()
    assert prompt.user_input == 'n'
    assert prompt.is_running
    # second interaction
    monkeypatch.setattr('builtins.input', lambda _: 'Q')
    prompt.run()
    assert prompt.user_input == 'Q'
    assert prompt.is_running, 'Looks like it was confused with q'
    # third interaction
    monkeypatch.setattr('builtins.input', lambda _: 'q uerty')
    prompt.run()
    assert prompt.user_input == 'q uerty'
    assert prompt.is_running, 'Ĺooks like it was confused with q'
