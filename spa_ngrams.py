#!/usr/bin/env python3

with open("./sentence-collector.txt") as input_file:
    sentences = [line.rstrip() for line in input_file]

words = []
for sentence in sentences:
	for word in sentence.rsplit():
		words.append(word)


print(words)

