# Name: pysentencizer.py
# Purpose: A simple sentencizer, tokenizer, and parts-of-speech tagger for the English language.
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

import string
import sys
import os.path
import distutils.sysconfig

PACKAGE="pysentencizer"
LOCAL="en"
SENTENCE_TERMINATORS = (".", "?", "!")
COMMON_ABBR = ("mr", "mstr", "miss", "mrs", "ms", "dr")
VERB = 1
NOUN = 2
PRONOUN = 3
ADJECTIVE = 4
ADVERB = 5
PREPOSITION = 6
CONJUNCTION = 7
INTERJECTION = 8

class BrillLexicon(object):
	def __init__(self, fileName=None):
		self.lexicon = {}

		packageFileName = str(distutils.sysconfig.get_python_lib())+"/"+PACKAGE+"/"+LOCAL+"/brill-lexicon.dat"
		localFileName = PACKAGE+"/"+LOCAL+"/brill-lexicon.dat"

		if fileName != None:
			pass
		elif os.path.isfile(packageFileName):
			fileName = packageFileName
		elif os.path.isfile(localFileName):
			fileName = localFileName
		else:
			sys.stderr.write("ERROR: Could not find default Brill lexicon.")

		lexiconFile = open(fileName, "r")
		for line in lexiconFile.readlines():
			if not line.startswith("#"):
				col = line.split()
				self.lexicon[col[0]] = col[1:]

	def getBrillTags(self, word):
		return self.lexicon.get(word, [])

	def getPos(self, token):
		if token.brillTag == "CC":
			return CONJUNCTION
		elif token.brillTag == "CD":
			return ADJECTIVE
		elif token.brillTag == "DT":
			return ADJECTIVE
		elif token.brillTag == "EX":
			return ADVERB
		elif token.brillTag == "FW":
			return NOUN
		elif token.brillTag == "IN":
			return PREPOSITION
		elif token.brillTag.startswith("J"):
			return ADJECTIVE
		elif token.brillTag == "LS":
			return NOUN
		elif token.brillTag == "MD":
			return VERB
		elif token.brillTag.startswith("N"):
			return NOUN
		elif token.brillTag == "PDT":
			return ADJECTIVE
		elif token.brillTag == "POS":
			return NOUN
		elif token.brillTag.startswith("P"):
			return PRONOUN
		elif token.brillTag.startswith("RB"):
			return ADVERB
		elif token.brillTag == "RP":
			return VERB
		elif token.brillTag == "SYM":
			return NOUN
		elif token.brillTag == "to":
			return PREPOSITION
		elif token.brillTag == "UH":
			return INTERJECTION
		elif token.brillTag.startswith("V"):
			return VERB
		elif token.brillTag == "WDT":
			return ADJECTIVE
		elif token.brillTag.startswith("WP"):
			return PRONOUN
		elif token.brillTag == "WRB":
			return ADVERB
		elif token.brillTag == "TO":
			return PREPOSITION

class Token(object):
	def __init__(self, value, source, sourceIndex, nextToken=None):
		self.value = value
		self.source = source
		self.sourceIndex = sourceIndex
		self.nextToken = nextToken

		self.isSentenceStart = False
		self.isSentenceEnd = False
		self.isParaStart = False
		self.isParaEnd = False
		self.isWord = False
		self.isCapital = False
		self.isNumber = False
		self.isPunctuation = False
		self.isAbbr = False
		self.isAcronym = False
		self.isSpaceFollows = False
		
		self.brillTag = None
		self.pos = None

	def getRawText(self):
		if self.nextToken == None:
			return self.source[self.sourceIndex:]
		else:
			return self.source[self.sourceIndex:self.nextToken.sourceIndex]

	def __str__(self):
		return self.value

	def __repr__(self):
		repr = "'"+self.__str__()+"'"
		if self.isSentenceStart:
			repr += "/sent_start"
		if self.isSentenceEnd:
			repr += "/sent_end"
		if self.isParaStart:
			repr += "/para_start"
		if self.isParaEnd:
			repr += "/para_end"
		if self.isWord:
			repr += "/word"
		if self.isCapital:
			repr += "/capital"
		if self.isNumber:
			repr += "/number"
		if self.isPunctuation:
			repr += "/punc"
		if self.isAbbr:
			repr += "/abbr"
		if self.isAcronym:
			repr += "/acronym"
		if self.pos == VERB:
			repr += "/verb"
		if self.pos == NOUN:
			repr += "/noun"
		if self.pos == PRONOUN:
			repr += "/pronoun"
		if self.pos == ADJECTIVE:
			repr += "/adjective"
		if self.pos == ADVERB:
			repr += "/adverb"
		if self.pos == PREPOSITION:
			repr += "/preposition"
		if self.pos == CONJUNCTION:
			repr += "/conjunction"
		if self.pos == INTERJECTION:
			repr += "/interjection"
		if self.brillTag != None:
			repr += "/"+self.brillTag
		return repr

class Sentencizer(object):
	def __init__(self, brillLexicon="default"):
		if brillLexicon == "default":
			self.brillLexicon = BrillLexicon()
		else:
			self.brillLexicon = brillLexicon

	def sentencize(self, inputString):
		### first pass, generate tokens
		def appendToken(inputString, tokens, tokenValue, i):
			token = Token(tokenValue, inputString, i)
			if len(tokens) > 0:
				tokens[-1].nextToken = token
			tokens.append(token)
		tokens = []
		tokenValue = None
		tokenIndex = 0
		isTokenAlphanum = False
		for i in range(len(inputString)):
			c = inputString[i]
			if c in string.whitespace:
				if tokenValue != None:
					appendToken(inputString, tokens, tokenValue, tokenIndex)
					tokenValue = None
			elif c in string.punctuation:
				if tokenValue != None:
					appendToken(inputString, tokens, tokenValue, tokenIndex)
					tokenValue = None
				tokenValue = c
				tokenIndex = i
				isTokenAplhanum = False
			else:
				if tokenValue == None:
					tokenValue = c
					tokenIndex = i
					isTokenAplhanum = True
				elif isTokenAplhanum:
					tokenValue += c
				else:
					appendToken(inputString, tokens, tokenValue, tokenIndex)
					tokenValue = c
					tokenIndex = i
					isTokenAplhanum = True
		if tokenValue != None:
			appendToken(inputString, tokens, tokenValue, tokenIndex)

		### second pass, assign token properties
		for i in range(len(tokens)):
			if tokens[i].value.isalpha():
				tokens[i].isWord = True
				if tokens[i].value[0].isupper():
					tokens[i].isCapital = True
				if tokens[i].value.isupper():
					tokens[i].isAcronym = True
			if tokens[i].value.isdigit():
				tokens[i].isNumber = True
			if tokens[i].value in string.punctuation:
				tokens[i].isPunctuation = True
			if i+1 < len(tokens) and tokens[i].source[tokens[i+1].sourceIndex-1] in string.whitespace:
				tokens[i].isSpaceFollows = True

		### third pass, combine tokens and mark sentence start and end
		sentenceStarted = False
		parStarted = False
		i = 0
		while i < len(tokens):
			if not sentenceStarted:
				tokens[i].isSentenceStart = True
				sentenceStarted = True
			if not parStarted:
				tokens[i].isParaStart = True
				parStarted = True
			elif tokens[i].getRawText().count("\n") > 1:
				tokens[i].isParaEnd = True
				parStarted = False
			if tokens[i].value == "-" and not tokens[i].isSpaceFollows \
				and i > 0 and tokens[i-1].isWord and not tokens[i-1].isSpaceFollows \
				and i+1 < len(tokens) and tokens[i+1].isWord:
				tokens[i-1].value += tokens[i].value + tokens[i+1].value
				tokens[i-1].nextToken = tokens[i+1].nextToken
				del tokens[i:i+2]
				i -= 1
			elif tokens[i].value == "'" and not tokens[i].isSpaceFollows \
				and i > 0 and tokens[i-1].isWord and not tokens[i-1].isSpaceFollows \
				and i+1 < len(tokens) and tokens[i+1].isWord:
				tokens[i-1].value += tokens[i].value + tokens[i+1].value
				tokens[i-1].nextToken = tokens[i+1].nextToken
				tokens[i-1].isWord = True
				del tokens[i:i+2]
				i -= 1
			elif tokens[i].value in SENTENCE_TERMINATORS:
				# e.g. and i.e.
				if tokens[i].value == "." and not tokens[i].isSpaceFollows \
					and i > 0 and tokens[i-1].isWord and not tokens[i-1].isSpaceFollows \
					and i+1 < len(tokens) and tokens[i+1].isWord:
					tokens[i-1].value += tokens[i].value + tokens[i+1].value
					tokens[i-1].nextToken = tokens[i+1].nextToken
					del tokens[i:i+2]
					i -= 1
				# common abbriviations "Mr."
				elif tokens[i].value == "."  and i > 0 and tokens[i-1].value.lower() in COMMON_ABBR:
					tokens[i-1].isAbbr = True
					tokens[i-1].value += "."
					tokens[i-1].nextToken = tokens[i].nextToken
					del tokens[i]
				# other things that look more like an abreviation than a sentence end
				elif tokens[i].value == "." and not (i+1 == len(tokens)) \
					and not (tokens[i+1].isCapital or tokens[i+1].value == "\""):
					tokens[i-1].isAbbr = True
					tokens[i-1].value += tokens[i].value
					tokens[i-1].nextToken = tokens[i].nextToken
					del tokens[i]
				# sentence ends with abbreviation
				elif tokens[i].value == "." and i > 0 and tokens[i-1].value == "etc":
					tokens[i-1].isAbbr = True
					tokens[i-1].value += tokens[i].value
					tokens[i-1].nextToken = tokens[i].nextToken
					tokens[i-1].isSentenceEnd = True
					del tokens[i]
				# sentence ends with ellipsis
				elif tokens[i].value == "." and i+2 < len(tokens) and tokens[i+1].value == "." and tokens[i+2].value == ".":
					tokens[i].value = "..."
					tokens[i].nextToken = tokens[i+2].nextToken
					tokens[i].isSentenceEnd = True
					del tokens[i+1:i+3]
				# sentence ends with closing "
				elif i+1 < len(tokens) and tokens[i+1].value == "\"" and not tokens[i+1].source[tokens[i+1].sourceIndex-1] in string.whitespace:
					tokens[i+1].isSentenceEnd = True
				# sentence ends with . or ! or ?
				else:
					tokens[i].isSentenceEnd = True
			if i < len(tokens) and tokens[i].isSentenceEnd:
				sentenceStarted = False
			i += 1
		if len(tokens) > 0:
			tokens[-1].isParaEnd = True

		### fourth pass, assign parts of speech from lexicon
		if self.brillLexicon != None:
			for word in tokens:
				if word.isWord:
					brillTags = self.brillLexicon.getBrillTags(word.value)
					if len(brillTags) == 0 and word.isSentenceStart:
						brillTags = self.brillLexicon.getBrillTags(word.value.lower())

					if len(brillTags) > 0:
						word.brillTag = brillTags[0]
						word.pos = self.brillLexicon.getPos(word)
					else:
						word.brillTag = "NN"
						word.pos = NOUN

		### fith pass, preform Brill transition rules
		if self.brillLexicon != None:
			lastWord = None
			for word in tokens:
				if word.isWord:
					# some common transition rules from Eric Brill
					# rule 1: NN --> NNS if has suffix -s
					if word.brillTag == "NN" and word.value.endswith("s"):
						word.brillTag = "NNS"
					# rule 2: NN --> CD if has character .
					if word.brillTag == "NN" and word.value.find(".") != -1:
						word.brillTag = "CD"
					# rule 3: NN --> JJ if has character -
					if word.brillTag == "NN" and word.value.find("-") != -1:
						word.brillTag = "JJ"
					# rule 4: NN --> VBN if has suffix -ed
					if word.brillTag == "NN" and word.value.endswith("ed"):
						word.brillTag = "VBN"
					# rule 5: NN --> VBG if has suffix -ing
					if word.brillTag == "NN" and word.value.endswith("ing"):
						word.brillTag = "VBG"
					# rule 6: ?? --> RB if has suffix -ly
					if word.value.endswith("ly"):
						word.brillTag = "RB"
					# rule 7: ?? --> JJ if adding suffix -ly results in a word
					if self.brillLexicon.getBrillTags(word.value+"ly") != []:
						word.brillTag = "JJ"
					# rule 8: NN --> CD the word $ can appear to the left
					if word.brillTag == "NN" and word.value.startswith("$"):
						word.brillTag = "CD"
					# rule 9: NN --> JJ if has suffix -al
					if word.brillTag == "NN" and word.value.endswith("al"):
						word.brillTag = "JJ"
					# rule 10: NN --> VB if the word would appears to the left
					if word.brillTag == "NN" and lastWord and lastWord.value == "would":
						word.brillTag = "VB"
					# rule 11: NN --> CD if has character 0
					if word.brillTag == "NN" and word.value.find("0") != -1:
						word.brillTag = "CD"
					# rule 12: NN --> JJ if the word be appears to the left
					if word.brillTag == "NN" and lastWord and lastWord.value == "be":
						word.brillTag = "JJ"
					# rule 13: NNS --> JJ if has suffix -us
					if word.brillTag == "NNS" and word.value.endswith("us"):
						word.brillTag = "JJ"
					# rule 14: NNS --> VBZ if the word it appears to the left
					if word.brillTag == "NNS" and lastWord and lastWord.value == "it":
						word.brillTag = "VBZ"
					# rule 15: NN --> JJ if has suffix -ble
					if word.brillTag == "NN" and word.value.endswith("ble"):
						word.brillTag = "JJ"
					# rule 16: NN --> JJ if has suffix -ic
					if word.brillTag == "NN" and word.value.endswith("ic"):
						word.brillTag = "JJ"
					# rule 17: NN --> CD has character 1
					if word.brillTag == "NN" and word.value.find("1") != -1:
						word.brillTag = "CD"
					# rule 18: NNS --> NN if has suffix -ss
					if word.brillTag == "NNS" and word.value.endswith("ss"):
						word.brillTag = "NN"
					# rule 19: ?? --> JJ if deleting un- results in a word
					if word.value.startswith("un") and self.brillLexicon.getBrillTags(word.value[2:]) != []:
						word.brillTag = "JJ"
					# rule 20: NN --> JJ if has suffix -ive
					if word.brillTag == "NN" and word.value.endswith("ive"):
						word.brillTag = "JJ"

					word.pos = self.brillLexicon.getPos(word)
					lastWord = word
		return tokens
