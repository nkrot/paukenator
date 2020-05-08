
class Challenge(object):
    """A test item -- a question and all user answers to it"""

    def __init__(self, hidden_word, **kwargs):
        self.word = hidden_word # (pos, word, hidden_representation)
        self.max_attempts = kwargs.get('max_attempts', 1)
        # A caller is the object that runs the challenge, typically a Prompt.
        self.caller = kwargs.get('caller', None)
        # information about the collection of challenges to which this very
        # challenge belongs:
        # * position of this very challenge in the collection (starting from 1)
        # * total number of challenges in the collection
        self.info = (1,1) # TODO: think of a better name

        self.debug = False
        self.skipped = False

        # should not be updated from outside
        # TODO: make them private
        self.current_attempt = 0
        self.user_inputs = []
        self.checked_user_inputs = []

    # TODO
    # def run(self):
    #     while not self.finished:
    #         self.make_attempt()
    #     raise StopIteration

    def question(self):
        """Generate text of the question that will be shown to the user."""
        tpl = "Question #{} of {}. To answer, please type in a suitable word."
        return tpl.format(self.info[0], self.info[1])

    def make_attempt(self):
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

    def analyse_answer(self):
        """Analyse the most recent answer."""
        self.checked_user_inputs.append(self.answer == self.correct_answer)
        if self.answered_correctly:
            print("  CORRECT!")
        elif self.current_attempt == self.max_attempts:
            print(f"  Wrong. Correct answer is: {self._correct_answer}")
        else:
            print("  Wrong. Try again.")
        pass

    def skip(self, rude=False):
        """Mark the challenge as skipped."""
        self.skipped = True
        title = "SHAME ON YOU, DAMN COWARD!" if rude else "COWARD!"
        print(f"  {title} Correct answer is: {self._correct_answer}")

    @property
    def finished(self):
        """
        Tell if the challenge has finished, which happens if
          * maximum number of attempts has been consumed
          * user's most recent answer was correct
          * user's most recent answer was to skip the challenge
        """
        return ( self.skipped
                 or self.current_attempt >= self.max_attempts
                 or self.answered_correctly )

    @property
    def answer(self):
        """Return the most recent answer given by the user"""
        return (self.user_inputs or [None])[-1]

    @property
    def correct_answer(self):
        return self.word[1]

    @property
    def _correct_answer(self):
        """Correct answer for showing in a message"""
        return self.word[1]

    @property
    def answered_correctly(self):
        """Tell if the most recent answer is correct"""
        return (self.checked_user_inputs or [None])[-1]

    def _debug(self, msg):
        if self.debug:
            print(msg)
