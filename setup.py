#!/usr/bin/env python
# Name: setup.py
# Purpose: Installation of pysentencizer.
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

from distutils.core import setup
import nltk

setup(
	name = "pysentencizer",
	description = "Sentencizer, tokenizer, and parts-of-speech tagger",
    
	version = "0.0.2",
	url = "http://matthew.tancreti.net/pySentencizer.html",
	long_description = "This Python module is a simple sentencizer, tokenizer, and parts-of-speech tagger for the English language.",
	license = "Apache License, Version 2.0",
	keywords = ["sentencizer", "sentence", "splitter", "tokenizer", "parts-of-speech", "pos", "tagger"],
	author = "Matthew Tan Creti",
	author_email = "mtancret@purdue.edu",
    
	package_data = {'pysentencizer': ['en/brill-lexicon.dat']},
    
	packages = ['pysentencizer']
)

