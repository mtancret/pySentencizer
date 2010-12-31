"""
Test sentencizing.

>>> print sentNoPos.sentencize("First. Second! Thrid?")
['First'/sent_start/para_start/word/capital, '.'/sent_end/punc, 'Second'/sent_start/word/capital, '!'/sent_end/punc, 'Thrid'/sent_start/word/capital, '?'/sent_end/para_end/punc]

Test paragraphs.

>>> print sentNoPos.sentencize("First paragraph.\\n\\nSecond paragraph.")
['First'/sent_start/para_start/word/capital, 'paragraph'/word, '.'/sent_end/para_end/punc, 'Second'/sent_start/para_start/word/capital, 'paragraph'/word, '.'/sent_end/para_end/punc]

Test abbreviations.

>>> print sentNoPos.sentencize("Mr. Jones.")
['Mr.'/sent_start/para_start/word/capital/abbr, 'Jones'/word/capital, '.'/sent_end/para_end/punc]

>>> print sentNoPos.sentencize("Foo i.e. bar e.g. etc.")
['Foo'/sent_start/para_start/word/capital, 'i.e.'/word/abbr, 'bar'/word, 'e.g.'/word/abbr, 'etc.'/sent_end/para_end/word/abbr]

Test tagging.

>>> print sentPos.sentencize("Go.")
['Go'/sent_start/para_start/word/capital/verb/VB, '.'/sent_end/para_end/punc]

>>> print sentPos.sentencize("Hark! He read quickly at the magic fountain.")
['Hark'/sent_start/para_start/word/capital/interjection/UH, '!'/sent_end/punc, 'He'/sent_start/word/capital/pronoun/PRP, 'read'/word/verb/VB, 'quickly'/word/adverb/RB, 'at'/word/preposition/IN, 'the'/word/adjective/DT, 'magic'/word/adjective/JJ, 'fountain'/word/noun/NN, '.'/sent_end/para_end/punc]

Test unusual inputs.

>>> print sentPos.sentencize("")
[]

>>> print sentPos.sentencize(".")
['.'/sent_start/sent_end/para_start/para_end/punc]
"""

import pysentencizer
sentNoPos = pysentencizer.Sentencizer(None)
sentPos = pysentencizer.Sentencizer()

if __name__ == "__main__":
	import doctest
	doctest.testmod()

