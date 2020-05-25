from collections import defaultdict
from typing import Dict

from paukenator.report import Report
from paukenator.exercises import Exercise


class SimplePrompt(object):
    COMMANDS: Dict[str, str] = {
        'q' : 'to quit',
        'r' : 'to repeat current sentence'
    }

    def __init__(self):
        self.user_input = None
        self._exercise = None
        self.debug = False
        self.counts = defaultdict(int)
        self.text = None  # some derived classes will need it
        self.is_interactive = False
        self._report = None
        # Is False iff the user pressed REPEAT previous time.
        self._is_new_example = True

    def description(self) -> str:
        return "non-interactive"

    @property
    def report(self) -> Report:
        return self._report

    @report.setter
    def report(self, val: Report) -> None:
        self._report = val
        self._report.answer_mode = self.description()
        self._report.answers_expected = self.is_interactive
        if self.exercise:
            self._report.exercise_type = self.exercise.description()

    @property
    def exercise(self) -> Exercise:
        return self._exercise

    @exercise.setter
    def exercise(self, ex: Exercise) -> None:
        self._exercise = ex
        if self._report:
            self._report.exercise_type = self._exercise.description()

    @property
    def is_running(self) -> bool:
        return self.user_input != 'q'

    @property
    def proceed(self) -> bool:
        # TODO: should it be False if the user pressed q?
        return self.user_input != 'r'

    # TODO: Refactor: create fake challenges, not for displaying but for
    # counting the questions (a question is a challenge).
    # For consistency with other types of Prompt, reading of user input will
    # can be accomplished inside Challenge object as well.

    def run(self) -> None:
        self._is_new_example = self.proceed
        self.user_input = input("> ")
        self._update_report()
        pass

    def help_message(self) -> str:
        msg = ", ".join([f"{k} {v}" for k, v in self.COMMANDS.items()])
        msg = f"HELP: Press {msg} or any other key to continue.\n"
        return msg

    def show_help(self) -> None:
        print(self.help_message())

    def goodbye(self) -> None:
        print("Good bye. Hope to see you soon again.")

    def _debug(self, msg: str) -> None:
        if self.debug:
            print(msg)

    def start(self) -> None:
        self.show_help()
        if self.report:
            self.report.start()

    def finish(self) -> None:
        if self.report:
            self.report.finish()

    def _update_report(self) -> bool:
        """Update counts in the report."""
        if self.report is None:
            return False
        if self.is_running and self._is_new_example:
            # Increment the count of studied sentences by one:
            # * not counting the sentence when the user typed QUIT
            # * counting repeated sentence only once
            self.report.incr_studied_sentences()
        if self.is_running:
            self.report.incr_asked_questions(len(self.exercise.hidden_words))

        return True
