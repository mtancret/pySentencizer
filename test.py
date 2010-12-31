"""
Test abbreviations

>>> print sentNoPos.sentencize("Mr. Jones.")
['Mr.'/sent_start/para_start/word/capital/abbr, 'Jones'/word/capital, '.'/sent_end/punc]

Test tagging

>>> print sentPos.sentencize("Go.")
['Go'/sent_start/para_start/word/capital/verb/VB, '.'/sent_end/punc]
"""

import pysentencizer
sentNoPos = pysentencizer.Sentencizer(None)
sentPos = pysentencizer.Sentencizer()

if __name__ == "__main__":
	import doctest
	doctest.testmod()

