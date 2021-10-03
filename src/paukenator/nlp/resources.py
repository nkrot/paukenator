# dictionaries used in tokenization
#
# TODO: organize it somehow better, preferably load from a text file

SEMDICT = {
    "deu": {
        # words that never occur at the end of a sentence
        # TODO: 'bzw.'
        'NO_SENT_END': {'z.B.', 'ca.', 'vgl.', 'bzgl.'},

        'MONTH_NAMES': {
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
        },

        'NOUNS_WITH_ORDINAL_NUMBER': {
            'Jahrhundert', 'Jahrhunderts', 'Jh.', 'Jh',
            'Weltjugendtag', 'Weltjugendtags'
        }
    }
}

SEMDICT['deu'].update({
   'ABBREVIATIONS': SEMDICT['deu']['NO_SENT_END']
})
