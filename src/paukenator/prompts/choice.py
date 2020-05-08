class Choice(object):
    def __init__(self, name, value, is_correct=False):
        self.name = name
        self.value = value
        self.correct = is_correct
        self.template = "option {}: {}"

    def __str__(self):
        return self.template.format(self.name, self.value)
