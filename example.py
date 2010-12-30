#!/usr/bin/python
import pysentencizer
import sys

input = sys.stdin.read()
tokens = pysentencizer.sentencize(input)
print tokens
for token in tokens:
	if token.isSentenceStart:
		sys.stdout.write("\n>>> ")
	text = token.getRawText().replace("\n"," ")
	sys.stdout.write(text)
	if token.isParaEnd:
		print
print
