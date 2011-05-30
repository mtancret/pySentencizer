# Name: test.py
# Purpose: Regression tests for pysentencizer.
# Author(s): Matthew Tan Creti
#
# Copyright 2010 Matthew Tan Creti
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

Test performance.

>>> print ((not TEST_PERFORMANCE) or (timeSentencizeWarAndPeace() < 60))
True
"""

import doctest
import time
import sys
import pysentencizer

TEST_PERFORMANCE = False

sentNoPos = pysentencizer.Sentencizer(None)
sentPos = pysentencizer.Sentencizer()

def timeSentencizeWarAndPeace():
	file = open("test/war-and-peace.txt", "r")
	text = file.read()
	start = time.time()
	sentPos.sentencize(text)
	stop = time.time()
	return stop - start

if __name__ == "__main__":
	print "Running tests."
	if len(sys.argv) > 1:
		if sys.argv[1] == "-p":
			TEST_PERFORMANCE = True	
		else:
			print "WARNING: Unknown option",sys.argv[1]
	else:
		print "Not testing performance. Use -p to run performance tests."

	doctest.testmod()

