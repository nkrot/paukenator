import random
from typing import List, Union, Optional

from .challenge import Challenge
from .choice import Choice


class MultipleChoiceChallenge(Challenge):

    @classmethod
    def description(cls):
        return "multiple-choice"

    def __init__(self, hidden_word, **kwargs):
        super().__init__(hidden_word, **kwargs)
        self.num_choices: int = 3
        self.choices: List[Choice] = None
        self.text: 'text.Text' = None
        self._correct_choice = None

    def __repr__(self):
        msg = "<{}: num_choices={} choices={} text={}>".format(
            self.__class__.__name__, self.num_choices, self.choices,
            self.text)
        return msg

    def question(self):
        """Generate text of the question that will be shown to the user.
        Example
        -------
        Question #1 of 2. To answer please type in a number of preferred \
        option (1, 2 or 3):
          option 1: alpha
          option 2: beta
          option 3: gamma
        """
        if self.choices is None:
            self.create_choices()
        options = [f" {choice}" for choice in self.choices]
        answers = self._spellorlist([choice.name for choice in self.choices])
        msg = "Question #{} of {}.".format(self.info[0], self.info[1])
        msg += " To answer, please type in the number of preferred option"
        msg += " ({}):".format(answers)
        msg += "\n{}".format("\n".join(options))
        return msg

    @property
    def correct_answer(self):
        return self._correct_choice.name

    @property
    def _correct_answer(self):
        """Correct answer for showing in a message, as num (word)"""
        return "{} ({})".format(self._correct_choice.name,
                                self._correct_choice.value)

    @property
    def user_answers_(self) -> List[Optional[str]]:
        """User answer resolved to its real value
        TODO: should be all answers the user gave to the challenge?
        """
        res = []
        for choice in self.choices:
            if choice.name == self.answer:
                res.append(choice.value)
        return res

    @property
    def correct_answer_(self) -> str:
        """Correct answer resolved to its real value"""
        return self._correct_choice.value

    def create_choices(self):
        """
        Generates list of numbered choices of size self.num_choices, each
        choice being a tuple (number, word, correct_or_not). Numbering starts
        with 1 to make the choices look more human friendly.
          [("1", "I", False), ("2", "love", False), ("3", "Linux", True) ]
        One of the choices is always the correct answer.
        """
        # TODO: what happens if we dont have enough unique words to generate
        # as many choices as required
        if self.text is None:
            self.text = self.caller.text
        candidates = self.text.words_no_punctuations()
        choices = set([self.word.text])  # add correct answer
        num_missing = self.num_choices - len(choices)
        while num_missing > 0:
            choices.update(random.sample(candidates, num_missing))
            num_missing = self.num_choices - len(choices)

        # convert to Choice object
        self.choices = random.sample(choices, len(choices))  # randomize
        self.choices = [Choice(str(i+1), wd, wd == self.word.text)
                        for i, wd in enumerate(self.choices)]
        self._correct_choice = next(ch for ch in self.choices if ch.correct)
        self._debug(self.choices)

    def _spellorlist(self, items):
        """
        Given a list, spell it out, for example:
        [1,2,3] --> 1, 2 or 3
        """
        seps = [''] + [', '] * (len(items) - 2) + [' or ']
        return "".join([f"{s}{w}" for s, w in zip(seps, items)])
