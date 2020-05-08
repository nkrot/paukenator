import pytest

from paukenator.lesson import Lesson

# TODO:
#- move common fixtures to conftest.py
#- test that at least one word is hidden even if the sentence is too short
#- test hide_ratio works
#- test that all words are hidden of hide_ratio = 1
#- test that setting hide_ration to >1 is illegal
#- test hide_mode=partial
#- test what is never hidden: punctuation or commands valid to the current Prompt
#- test COMMANDS word as expected. how to emulate user input?
