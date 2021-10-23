# dictionaries used in tokenization
#
# TODO: organize it somehow better, preferably load from a text file

__version__ = '1'

SEMDICT = {
    "deu": {
        # words that never occur at the end of a sentence
        # TODO: 'bzw.'
        'NO_SENT_END': ['z.B.', 'ca.', 'vgl.', 'bzgl.'],

        'MONTH_NAME': [
            'Januar',    'Jan.',
            'Februar',   'Feb',
            'März',      'Mär.',
            'April',     'Apr.',
            'Mai',
            'Juni',      'Jun.',
            'Juli',      'Jul.',
            'August',    'Aug.',
            'September', 'Sep.', 'Sept.',
            'Oktober',   'Okt.',
            'November',  'Nov.',
            'Dezember',  'Dez.'
        ],

        'NOUN_WITH_ORDINAL_NUMBER': [
            'Jahrhundert', 'Jahrhunderts', 'Jh.', 'Jh',
            'Weltjugendtag', 'Weltjugendtags'
        ]
    },

    "eng": {
        'MONTH_NAME': ['Jan.', 'Feb.'],
        'ABBREVIATION': ['Dr.'],
        'NO_SENT_END': []
    }
}

SEMDICT['deu'].update({
   'ABBREVIATION': SEMDICT['deu']['NO_SENT_END']
})
