from collections import defaultdict

from paukenator.prompts import SimplePrompt, InteractivePrompt
from paukenator.prompts.challenges import Challenge, MultipleChoiceChallenge
from paukenator.exercises import FillInTheGaps
from paukenator.report import Report


class Lesson(object):
    HIDE_RATIO = 0.1

    NON_INTERACTIVE = "N"
    INTERACTIVE     = "I"
    MULTIPLE_CHOICE = "M"

    TEST_MODES = (
        ('N', 'non-interactive',
         'the user is asked a question but is not prompted to type in an answer'),
        ('I', 'interactive',
         'the user is asked a question and is prompted to type in an answer.'),
        ('M', 'multiple-choice',
         'the user is asked a quesiton and is prompted to select one answer from given set of answers.'),
    )

    DEFAULT_TEST_MODE = 'N'

    def __init__(self, text, config, **kwargs):
        self.text = text
        self.config = config
        self.prompt_mode = self.config.testmode or self.DEFAULT_TEST_MODE
        self.selector = self.config.selector

        self.prompt = None
        self.counts = defaultdict(int)

    def run(self):
        self.prompt = self._create_prompt()
        self.prompt.start()

        sentences = self.selector(self.text.sentences)

        c_curr, c_all = 0, len(sentences)
        num_sents_in_text = len(self.text.sentences)
        sentences = iter(sentences)
        sentence = None

        while self.prompt.is_running:
            if self.prompt.proceed:
                try:
                    sentence = next(sentences)
                    c_curr += 1
                except StopIteration:
                    break

            self.prompt.exercise = self._create_exercise(sentence)

            # show the exercise
            # TODO: move this into Prompt or Exercise?
            msg = "----- Sentence {} of {} (sentence #{} of {}) -----"
            print(msg.format(c_curr, c_all, 1+sentence.num, num_sents_in_text))
            print(self.prompt.exercise)

            # process user input
            self.prompt.run()

            # show the correct answer (full sentence)
            print(sentence)
            print()

        self.prompt.finish()
        print(self.prompt.report)

        self.prompt.goodbye()

    def _create_exercise(self, sentence):
        return FillInTheGaps(sentence, self.config,
                             number_gaps=self.prompt.is_interactive,
                             exceptions=self.prompt.COMMANDS.keys())

    def _create_prompt(self):
        """Create and return prompt according to the current prompt mode."""
        if self.prompt_mode == self.NON_INTERACTIVE:
            prompt = SimplePrompt()
        elif self.prompt_mode == self.INTERACTIVE:
            prompt = InteractivePrompt()
            prompt.challenge_class = Challenge
        elif self.prompt_mode == self.MULTIPLE_CHOICE:
            # TODO: refactor. If Prompt never uses .text for itself, it should
            # never know about it. Perhaps the pattern Prototype can be applied
            # here: we create a half-baked MultipleChoiceChallenge() with .text
            # and then create any new real Challenge by copying the prototype.
            # Alternatively, something like Factory Method, e.g.
            # MultipleChoiceChallengeMaker(text) with create_challenge() method
            prompt = InteractivePrompt()
            prompt.text = self.text  # will be used by MultipleChoiceChallenge
            prompt.challenge_class = MultipleChoiceChallenge
        else:
            raise ValueError(f"Unknown prompt mode: {self.prompt_mode}")
        # TODO: the order of setting attributes is important: report must be
        # the last one to set, at least after challenge_class has been set.
        prompt.report = Report()
        prompt.report.text = self.text
        return prompt

