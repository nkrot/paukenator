import re


class HiddenWord(object):
    NOWORD = "..."

    FULL = 1
    PARTIAL = 2

    @staticmethod
    def is_always_visible(text):
        """
        Tell if given :text should never be hidden from a sentence, like
        if the :text
         * is a punctuation mark
         * TODO: exceptions given from outside?
        """
        return bool(re.match(r'\W+$', text))

    def __init__(self, text, pos, **kwargs):
        self.text = text
        self.position = pos
        self.hide_mode = kwargs.get('hide_mode', self.FULL)
        self.include_position = kwargs.get('include_position', False)
        self.hidden = self._generate_hidden_representation()

    def __str__(self):
        return self.hidden

    def _generate_hidden_representation(self):
        """Transform given :word to hidden representation (aka "gap", "blank").
        In its basic form, hidden representation is just ellipsis:
          * computer --> ...
        but can also be partially hidden, e..g
          * computer --> c..r
          * tie      --> t..
        In any of interactive modes, it is useful to include a number into such
        hidden representation to ensure that the are nonambiguously indendified
        in case there are more than one gap in a single sentence:
          * computer --> <<1 c..r >>  (partially hidden)
          * tip      --> <<5 ... >>   (fully hidden)
        The gaps are numbered starting from 1 to make it human-friendly.

        TODO: select randomly which characters will be kept visible?
        """
        hidden = self.NOWORD
        if self.hide_mode == self.PARTIAL:
            if len(self.text) > 3:
                hidden = self.text[0] + self.NOWORD + self.text[-1]  # c..r
            else:
                hidden = self.text[0] + self.NOWORD[0:2]  # t..
        if self.include_position:
            # ex: <<2 ... >> or <<2 A...e >>
            hidden = f"<<{self.position+1} {hidden} >>"
        return hidden
