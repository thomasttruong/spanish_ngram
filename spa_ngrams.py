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
        phonemic_word = epi.transliterate(new_word)
        words.append(phonemic_word)

def make_ngram_dict(n):
    #TODO make modular lol,
    # only workd with unigrams :)
    dict_ngrams = dict()
    boundary_symbol = ''
    for i in range(n-1):
        boundary_symbol += 'ϵ'
    for word in words:
        word = [boundary_symbol] + word + [boundary_symbol]
    
    for character in word_split:
        dict_ngrams[character] = dict_ngrams.get(character, 0) + 1
    
    return dict_ngrams
