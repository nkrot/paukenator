from collections import defaultdict
from .simple_prompt import SimplePrompt

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

    @property
    def skip_word(self):
        return self.user_input == 's'

    @property
    def skip_sentence(self):
        return self.user_input == 'S'

    def read_input(self):
        # TODO: make each challenge + answer a separate class? it is like test case :)
        if not self.hidden_words:
            raise ValueError("No words to hide given")
        self._debug(self.hidden_words)
        for i,wd in enumerate(self.hidden_words):
            print(f"Word #{1+i} of {len(self.hidden_words)}")
            for t in range(self.max_attempts):
                last_attempt = self.max_attempts == t+1
                msg = f"- try {1+t} of {self.max_attempts} > "
                answer = input(msg).strip()
                self._debug(f"You answered: {answer}")
                if self._is_command(answer):
                    if self.skip_word:
                        print(f"  COWARD! Correct answer is: {wd[-1]}")
                        self._count_as_skipped()
                        break
                    elif self.skip_sentence:
                        self._count_as_skipped(len(self.hidden_words) - i)
                        print(f"  SHAME ON YOU, DAMN COWARD! Correct answer is: {wd[-1]}")
                        return False
                    else:
                        return False
                elif answer == wd[-1]:
                    print("  CORRECT!")
                    self._count_as_correct()
                    break
                elif last_attempt:
                    print(f"  Wrong. Correct answer is: {wd[-1]}")
                    self._count_as_incorrect()
                else:
                    print("  Wrong. Try again")
        return True

    def _is_command(self, answer):
        if answer in self.COMMANDS.keys():
            self.user_input = answer
            return True
        return False

    def help_message(self):
        msg = ", ".join([f"{k} {v}" for k,v in self.COMMANDS.items()])
        msg = f"HELP: Type a word or press {msg}.\n"
        return msg

    def _count_as_correct(self, v=1):
        self.counts['answered'] += v
        self.counts['correct']  += v

    def _count_as_incorrect(self, v=1):
        self.counts['answered']  += v
        self.counts['incorrect'] += v

    def _count_as_skipped(self, v=1):
        self.counts['skipped'] += v
