class CmpBase(object):
    '''Base class for comparators'''

    def __init__(self):
        self.equal = False
        self.debug = False

    def __repr__(self):
        return "<{}>".format(self.__class__.__name__)

    def __call__(self, expected, observed):
        '''Performs comparison of <expected> and <observed> and sets
        self.equal correspondingly.
        '''
        raise RuntimeError('Subclass must override this method')

    def no_diff(self) -> bool:
        '''Return True if the most recent comparison did not find any
        difference between objects being compared.
        '''
        return self.equal

    def has_diff(self) -> bool:
        '''Return True if the most recent comparison detected difference
        between objects being compared.
        '''
        return not(self.equal)

    def diff_as_string(self):
        '''Serialize difference to a string (one or multiline)'''
        raise RuntimeError('Subclass must override this method')
