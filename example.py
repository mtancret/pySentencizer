#!/usr/bin/python
import pysentencizer
import sys

input = sys.stdin.read()

senticizer = pysentencizer.Sentencizer()
tokens = senticizer.sentencize(input)
print tokens

for token in tokens:
	if token.isSentenceStart:
		print "\n>>> ",
	text = token.getRawText().replace("\n"," ").replace("\r","")
	sys.stdout.write(text)
	if token.isParaEnd:
		print
print
