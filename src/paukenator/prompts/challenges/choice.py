class Choice(object):
    def __init__(self, name, value, is_correct=False):
        self.name = name
        self.value = value
        self.correct = is_correct
        self.template = "option {}: {}"

    def __str__(self):
        return self.template.format(self.name, self.value)

    def __repr__(self):
        return "<{}: name={} value={} correct?={}>".format(
            self.__class__.__name__, self.name, self.value, self.correct)
