==========
Paukenator
==========

Paukenator (from German pauken - to cram, to drill) is a console tool for
practicing with texts, initially, texts in a foreign language. It aims at
helping in:

* practicing vocabulary and grammar
* memorizing the text

In brief, the tool will hide some words in a sentence and ask the student to
fill in the blanks. In one of the practice modes, the answers need to be typed
in literally, in another mode -- selected from given list ("multiple choice"),
for example:

.. code:: text

    ----- Sentence 1 of 6 (sentence #1 of 6) -----
    <<1 ... >> deutsche Sprache bzw . Deutsch ist eine plurizentrische westgermanische
     Sprache , die weltweit <<2 ... >> 90 bis 105 Millionen Menschen <<3 ... >> Muttersprache
     und weiteren rund 80 Millionen als Zweit - oder Fremdsprache dient .
    Question #1 of 3. To answer, please type in the number of preferred option (1, 2 or 3):
     option 1: Bundesdeutsch
     option 2: Sprachraum
     option 3: Die
    - try 1 of 2 > 1
      Wrong. Try again.
    - try 2 of 2 > 3
      CORRECT!
    Question #2 of 3. To answer, please type in the number of preferred option (1, 2 or 3):
     option 1: zusammen
     option 2: etwa
     option 3: sowie
    - try 1 of 2 >

The number of blanks, the mode of practicing and some other (for the time being,
only a few) things can be configured on the command line or via a configuration
file, an example of which is `<docs/lesson.ini>`_. To try the tool out:

.. code:: shell

    $ paukenator --hide-ratio 0.2 -c docs/lesson.ini docs/text.deu.sent.txt

To get help on usage:

.. code:: bash

    $ paukenator --help

Text Preprocessing
------------------

In paukenator tool, a minimal unit from which an exercise is built is one sentence.
The text is therefore expected to be one sentence per line.
There is a plan to provide the functionality of splitting into sentences, but
for the time being this should rather be done manually.

Empty lines are allowed in the text and indicate paragraphs. However, this is
not used in any manner for the time being.

Line comments introduced by a hash (#) sign are excluded from exercises.

Functionality in Brief
----------------------

Also described in `<docs/lesson.ini>`_ file.

* Choosing mode of exercising: non-interactive, interactive, multiple-choice

* Controlling the amount of words that will be replaced with blanks.

* Selecting type of blanks: full, partial.

* Selecting range of sentences to practice.





