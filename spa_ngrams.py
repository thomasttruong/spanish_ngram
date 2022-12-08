#!/usr/bin/env python3

import epitran
import string
import matplotlib.pyplot as plt
import numpy as np

words = []

def main():
    epi = epitran.Epitran('spa-Latn')
    punct = "«».,!¡?¿\"\';:\u200b“”\xad…&_"

    # read input file
    with open("./sentence-collector.txt") as input_file:
        sentences = [line.rstrip() for line in input_file]

    # make a list of all words
    for sentence in sentences:
        for word in sentence.rsplit():
            # remove punctuation
            new_word = word.translate(str.maketrans('', '', punct))
            # convert to ipa
            phonemic_word = epi.transliterate(new_word)

            words.append(phonemic_word)

    unigram_dict = make_ngram_dict(1)
    bigram_dict  = make_ngram_dict(2)
    trigram_dict = make_ngram_dict(3)

    make_frequency_plot(unigram_dict, 'Unigram')
    make_frequency_plot(bigram_dict, 'Bigram')
    make_frequency_plot(trigram_dict, 'Trigram')

def make_ngram_dict(n):
    dict_ngrams = dict()

    # change number of boundary symbols depending on n-gram
    boundary_symbol = ''
    for i in range(n-1):
        boundary_symbol += 'ϵ'

    # add boundary symbol to each word
    for word in words:
        word = boundary_symbol + word + boundary_symbol
        padded_words_list = []
        for i in range(n):
            padded_words_list.append(word[i:])
        ngrams = tuple(zip(*padded_words_list))
        for ngram in ngrams:
            dict_ngrams[ngram] = dict_ngrams.get(ngram, 0) + 1
    
    return dict_ngrams

def make_frequency_plot(dict_ngrams, title):
    # sort the dictionary
    sorted_ngrams = dict(sorted(dict_ngrams.items(), key=lambda x:x[1], reverse=True))
    # convert keys from tuples into strings
    ngram_keys = ["".join(tup) for tup in sorted_ngrams.keys()]
    curr_fig = plt.figure(1, figsize = (300, 8))
    plt.bar(ngram_keys, sorted_ngrams.values(), color='m', align = "edge", width = 0.3)
    plt.xticks(rotation = 90, size = 8)

    plt.title(f'{title} frequency for Spanish')
    plt.xlabel(f'{title}')
    plt.ylabel('Frequency')

    plt.savefig(f'plots/spa-{title.lower()}-freq.png')
    plt.clf()

if __name__=="__main__":
    main()
