#!/usr/bin/env python3

import epitran
import string

epi = epitran.Epitran('spa-Latn')
punct = ".,!¡?¿\"\';:"

with open("./sentence-collector.txt") as input_file:
    sentences = [line.rstrip() for line in input_file]

words = []
for sentence in sentences:
    for word in sentence.rsplit():
        # remove punctuation
        new_word = word.translate(str.maketrans('', '', punct))
        words.append(new_word)


print(words)

