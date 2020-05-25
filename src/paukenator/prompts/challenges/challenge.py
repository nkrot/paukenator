from typing import List, Union


class Challenge(object):
    """A test item -- a question and all user answers to it"""

    @classmethod
    def description(cls) -> str:
        return "type in the full answer"

    def __init__(self, hidden_word, **kwargs):
        self.word = hidden_word
        self.max_attempts = kwargs.get('max_attempts', 1)
        # A caller is the object that runs the challenge, typically a Prompt.
        self.caller = kwargs.get('caller', None)
        # information about the collection of challenges to which this very
        # challenge belongs:
        # * position of this very challenge in the collection (starting from 1)
        # * total number of challenges in the collection
        self.info = (1, 1)  # TODO: think of a better name

        self.debug = False
        self.skipped = False

        # should not be updated from outside
        # TODO: make them private
        self.current_attempt = 0
        self.user_inputs: List[str] = []
        self.checked_user_inputs: List[bool] = []

    # TODO
    # def run(self):
    #     while not self.finished:
    #         self.make_attempt()
    #     raise StopIteration

    def question(self) -> str:
        """Generate text of the question that will be shown to the user."""
        tpl = "Question #{} of {}. To answer, please type in a suitable word."
        return tpl.format(self.info[0], self.info[1])

    def make_attempt(self) -> None:
        """Perform a new attempt"""

        self.current_attempt += 1
        if self.current_attempt == 1:
            print(self.question())

        msg = f"- try {self.current_attempt} of {self.max_attempts} > "
        user_input = input(msg).strip()
        self.user_inputs.append(user_input)
        self._debug(f"You answered: {user_input}")

        if self.caller and self.caller.analyse_answer(self):
            # Let the caller object (a Prompt) recognize its own commands.
            pass
        else:
            self.analyse_answer()

    def analyse_answer(self) -> None:
        """Analyse the most recent answer."""
        self.checked_user_inputs.append(self.answer == self.correct_answer)
        if self.answered_correctly:
            print("  CORRECT!")
        elif self.current_attempt == self.max_attempts:
            print(f"  Wrong. Correct answer is: {self._correct_answer}")
        else:
            print("  Wrong. Try again.")
        pass

    def skip(self, rude=False) -> None:
        """Mark the challenge as skipped."""
        self.skipped = True
        title = "SHAME ON YOU, DAMN COWARD!" if rude else "COWARD!"
        print(f"  {title} Correct answer is: {self._correct_answer}")
        pass

    @property
    def finished(self) -> bool:
        """
        Tell if the challenge has finished, which happens if
          * maximum number of attempts has been consumed
          * user's most recent answer was correct
          * user's most recent answer was to skip the challenge
        """
        return (self.skipped
                or self.current_attempt >= self.max_attempts
                or self.answered_correctly)

    @property
    def answer(self) -> Union[str, None]:
        """Return the most recent answer given by the user"""
        # return (self.user_inputs or [None])[-1] # mypy sucks
        return self.user_inputs[-1] if self.user_inputs else None

    @property
    def correct_answer(self) -> str:
        return self.word.text

    @property
    def _correct_answer(self) -> str:
        """Correct answer for showing in a message"""
        return self.word.text

    @property
    def user_answers_(self) -> List[Union[str, None]]:
        """To be used in report
        TODO: should be all answers the user gave to the challenge
        """
        return [self.answer]

    @property
    def correct_answer_(self):
        """To be used in report"""
        return self.correct_answer

    @property
    def answered_correctly(self) -> bool:
        """Tell if the most recent answer was correct"""
        return (len(self.checked_user_inputs) > 0
                and self.checked_user_inputs[-1] is True)

    @property
    def answered_incorrectly(self) -> bool:
        """Return True if the most recent answer was not correct.
        Otherwise return False.

        Note that if the user did not attempt to answer, it does not count as
        incorrect answer and therefore False is returned.
        """
        return (len(self.checked_user_inputs) > 0
                and self.checked_user_inputs[-1] is False)

    @property
    def answered(self) -> bool:
        """Return true if the challenge was answered at least once, either
        correctly or incorrectly. Also understood as "attempted".

        If the user skipped/quit the challenge on the 1st attempt, this does
        not acount as answered (attempted).
        If the user skipped/quit the challenge upon the 2nd or any further
        attempts, this counts as answered (attempted).
        """
        return len(self.checked_user_inputs) > 0

    @property
    def asked(self) -> bool:
        return self.current_attempt > 0

    def _debug(self, msg) -> None:
        if self.debug:
            print(msg)
