from collections import defaultdict


class SimplePrompt(object):
    COMMANDS = {
        'q' : 'to quit',
        'r' : 'to repeat current sentence'
    }

    def __init__(self):
        self.user_input = None
        self.hidden_words = None
        self.debug = False
        self.counts = defaultdict(int)
        self.text = None  # some derived classes will need it

    @property
    def is_running(self):
        return self.user_input != 'q'

    @property
    def proceed(self):
        # TODO: should it be False if the user pressed q?
        return self.user_input != 'r'

    def run(self):
        self.user_input = input("> ")

    def help_message(self):
        msg = ", ".join([f"{k} {v}" for k, v in self.COMMANDS.items()])
        msg = f"HELP: Press {msg} or any other key to continue.\n"
        return msg

    def show_help(self):
        print(self.help_message())

    def goodbye(self):
        print("Good bye. Hope to see you soon again.")

    def _debug(self, msg):
        if self.debug:
            print(msg)
