from collections import defaultdict
from typing import Dict, Optional

from paukenator.prompts import SimplePrompt
from paukenator.exercises import HiddenWord
from paukenator.prompts.challenges import Challenge


class InteractivePrompt(SimplePrompt):
    COMMANDS: Dict[str, str] = {
        **SimplePrompt.COMMANDS,
        **{
            's' : 'to skip current word',
            'S' : 'to skip current sentence',
        }}

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.max_attempts = 2
        self.counts = defaultdict(int)
        self.challenge_class = Challenge
        self.is_interactive = True

    def description(self) -> str:
        return f"Interactive ({self.challenge_class.description()})"

    @property
    def skip_word(self) -> bool:
        return self.user_input == 's'

    @property
    def skip_sentence(self) -> bool:
        return self.user_input == 'S'

    def create_challenges(self) -> bool:
        """
        Set list of challenges `self.challenges` by creating Challenge objects
        from self.exercise.hidden_words.

        Return
        True if at least one was created
        False otherwise

        TODO: I would like to have this method private, but need to figure out
              how to test it w/o calling .run()
        """
        if not self.exercise:
            raise ValueError("Exercise not set. Cannot generate challenges.")
        if not self.exercise.hidden_words:
            raise ValueError("Hidden words not set."
                             " Cannot generate challenges.")
        self.challenges = [
            self.create_challenge(wd, idx)
            for idx, wd in enumerate(self.exercise.hidden_words)]
        return len(self.challenges) > 0

    def create_challenge(self, word: HiddenWord, idx: int) -> Challenge:
        """
        Create a challenge of required class and return it.
        """
        challenge = self.challenge_class(word)
        challenge.max_attempts = self.max_attempts
        challenge.caller = self
        challenge.info = (idx+1, len(self.exercise.hidden_words))
        return challenge

    def run(self) -> None:
        self._is_new_example = self.proceed
        self.user_input = None
        self.create_challenges()  # TODO: do it outside and inject?

        for idx, challenge in enumerate(self.challenges):
            if self.skip_sentence:
                # Mark all remaining challenges as skipped. (unused)
                challenge.skipped = True

            while not challenge.finished:
                challenge.make_attempt()
                if not self.is_running:  # react to QUIT
                    self._update_report()
                    return None

                # TODO: react to REPEAT? what is meaningful behaviour?

        self._update_report()
        pass

    def analyse_answer(self, challenge: Challenge) -> bool:
        """
        Analyse user input received, specifically, recognize own commands.

        Return
        ------
        True if the answer was recognized as own command
        False otherwise
        """
        if self._is_command(challenge.answer):
            if self.skip_word:
                challenge.skip()
            elif self.skip_sentence:
                challenge.skip(True)
            return True
        return False

    def _is_command(self, answer: Optional[str]) -> bool:
        if answer in self.COMMANDS.keys():
            self.user_input = answer
            return True
        return False

    def help_message(self) -> str:
        msg = ", ".join([f"{k} {v}" for k, v in self.COMMANDS.items()])
        msg = f"HELP: Type an answer or press {msg}.\n"
        return msg

    def _update_report(self) -> bool:
        """Update counts in the report."""
        if self.report is None:
            return False

        if self.is_running and self._is_new_example:
            # NOTE:
            # * not counting partially studied sentence, that is, when the user
            #   answered some questions but pressed QUIT before answering all
            #   of the questions from the sentence.
            # * counting SKIPPED sentences ('s' or 'S'). This is kind of
            #   inconsistent, because SKIPPED ('S' and all 's') is essentially
            #   the same as QUIT.
            # TODO: rethink the scope/definition of a studied sentence. Is it
            # (a) a sentence that has been shown to the user?
            # (b) a sentence that the user tried to answer at least once?
            # (c) a sentence that the user answered completely?
            # For now, a studied sentence is (a).
            self.report.incr_studied_sentences()

        for challenge in self.challenges:
            if challenge.asked:
                self.report.incr_asked_questions()

            if challenge.answered_correctly:
                self.report.incr_correctly_answered_questions()
                if challenge.current_attempt == 1:
                    self.report.incr_correctly_answered_questions_1st_attempt()
            elif challenge.answered_incorrectly:
                self.report.incr_incorrectly_answered_questions()
                self.report.add_incorrect_answer(challenge)
            # elif challenge.skipped:
            #     # TODO
            #     # The semantics of skipped is vague:
            #     # 1) asked/attempted once but chickened out?
            #     # 2) never attempted in a sentence that was shown?
            #     # 3) never attempted in future sentences/questions?
            #     self.report.incr_skipped_questions()

        return True
