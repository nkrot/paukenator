from collections import defaultdict
from paukenator.prompts import SimplePrompt
from paukenator.prompts.challenges import Challenge

class InteractivePrompt(SimplePrompt):
    COMMANDS = {
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

    @property
    def skip_word(self):
        return self.user_input == 's'

    @property
    def skip_sentence(self):
        return self.user_input == 'S'

    def create_challenges(self):
        """
        Set list of challenges `self.challenges` by creating Challenge objects
        from self.hidden_words.
        Return
        True if at least one was created

        TODO: I would like to have this method private, but need to figure out
              how to test it w/o calling .run()
        """
        if not self.hidden_words:
            raise ValueError("No hidden words (gaps/blanks) specified.")
        self.challenges = []
        for idx, wd in enumerate(self.hidden_words):
            challenge = self.challenge_class(wd)
            challenge.max_attempts = self.max_attempts
            challenge.caller = self
            challenge.info = (idx+1, len(self.hidden_words))
            self.challenges.append(challenge)
        return len(self.challenges) > 0

    def run(self):
        self.user_input = None
        self.create_challenges()  # TODO: do it outside and inject?

        for idx, challenge in enumerate(self.challenges):
            if self.skip_sentence:
                # Mark all remaining challenges as skipped. this will help
                # maintain correct counts.
                challenge.skipped = True

            while not challenge.finished:
                challenge.make_attempt()
                if not self.is_running:  # react to QUIT
                    self._update_counts()
                    return False

                # TODO: react to REPEAT? what is meaningful behaviour?

        self._update_counts()
        pass

    def analyse_answer(self, source):
        """
        Analyse user input received from a :source object (e.g. a Challenge),
        specifically, recognize own commands.

        Return
        ------
        True if the answer was recognized as own command
        False otehrwise
        """
        if self._is_command(source.answer):
            if self.skip_word:
                source.skip()
            elif self.skip_sentence:
                source.skip(True)
            return True
        return False

    def _is_command(self, answer):
        if answer in self.COMMANDS.keys():
            self.user_input = answer
            return True
        return False

    def help_message(self):
        msg = ", ".join([f"{k} {v}" for k, v in self.COMMANDS.items()])
        msg = f"HELP: Type an answer or press {msg}.\n"
        return msg

    def _update_counts(self):
        for challenge in self.challenges:
            if challenge.skipped:
                self._count_as_skipped()
            elif challenge.answered_correctly:
                self._count_as_correct()
            else:
                self._count_as_incorrect()

    def _count_as_correct(self, v=1):
        self.counts['answered'] += v
        self.counts['correct']  += v

    def _count_as_incorrect(self, v=1):
        self.counts['answered']  += v
        self.counts['incorrect'] += v

    def _count_as_skipped(self, v=1):
        self.counts['skipped'] += v
