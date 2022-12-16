#!/usr/bin/env python3

import epitran
import string
import matplotlib.pyplot as plt
import numpy as np
import random

words = []
terminator = 'ϵ' 

def main():
    # initialize
    epi = epitran.Epitran('spa-Latn')
    punct = "\t-«».,!¡?¿\"\';:\u200b“”\xad…&_"

    # read input file
    with open("data/sentence-collector.txt") as input_file:
        sentences = [line.rstrip() for line in input_file]

    # make a list of all words
    out_file = open("data/transcribed.txt", "w")
    for sentence in sentences:
        for word in sentence.rsplit():
            # remove punctuation
            new_word = word.translate(str.maketrans('', '', punct))
            # convert to ipa
            phonemic_word = epi.transliterate(new_word)

            words.append(phonemic_word)
            out_file.write(phonemic_word+'\n')
    out_file.close()

    # create sorted dictionaries of
    # unigrams, bigrams, and trigrams
    # where keys are tuples ('a', 'b', 'c')
    # and values are frequencies
    unigram_dict = make_ngram_dict(1)
    bigram_dict  = make_ngram_dict(2)
    trigram_dict = make_ngram_dict(3)

    make_frequency_plot(unigram_dict, 'Unigram')
    make_frequency_plot(bigram_dict, 'Bigram')
    make_frequency_plot(trigram_dict, 'Trigram')


    # prints 3 random words using bigram dictionary
    # of length 8
    print('Generating 3 words of length 8 using bigram dictionary')
    for j in range (3):
        print(random_bigram_word(bigram_dict, 8))

def make_ngram_dict(n):
    dict_ngrams = dict()

    # change number of boundary symbols depending on n-gram
    boundary_symbol = ''
    for i in range(n-1):
        boundary_symbol += terminator

    # add boundary symbol to each word
    for word in words:
        word = boundary_symbol + word + boundary_symbol
        padded_words_list = []
        for i in range(n):
            padded_words_list.append(word[i:])
        ngrams = tuple(zip(*padded_words_list))
        for ngram in ngrams:
            dict_ngrams[ngram] = dict_ngrams.get(ngram, 0) + 1

    # sort the dictionary
    sorted_ngrams = dict(sorted(dict_ngrams.items(), key=lambda x:x[1], reverse=True))

    return sorted_ngrams

def make_frequency_plot(sorted_ngrams, title):
    plot_title = f'{title} frequency in Spanish'
    file_path = f'plots/spa-{title.lower()}-freq.png'
    print(f'Making graph of {plot_title} and saving to {file_path}...')

    # convert keys from tuples into strings
    ngram_keys = ["".join(tup) for tup in sorted_ngrams.keys()]
    curr_fig = plt.figure(1, figsize = (300, 8))
    plt.bar(ngram_keys, sorted_ngrams.values(), color='m', align = "edge", width = 0.3)
    plt.xticks(rotation = 90, size = 8)

    plt.title(plot_title)
    plt.xlabel(f'{title}')
    plt.ylabel('Frequency')

    plt.savefig(file_path)
    plt.clf()
    
def random_bigram_word(bigram_dict, average_length):

    '''
    Input:
    bigram_dict: dicitonary of bigrams by their absolute frequency
    average_length: average length of a word in the dataset
    delta: variation between length of words

    Output:
    A random word based on the bigram frequencies
    '''

    total_bigrams = sum(bigram_dict.values())
    frequency_map = []
    index = 0
    for (bigram, abs_freq) in bigram_dict.items():
        for i in range(index, index + abs_freq):
            frequency_map.append(bigram)
        index = index + abs_freq
    res = ""
    for i in range(average_length):
        curr_bigram_pos = random.randint(0, total_bigrams)
        if res == "":
            res += terminator
            while (not word_start(frequency_map[curr_bigram_pos])) or word_end(frequency_map[curr_bigram_pos]):
                curr_bigram_pos = random.randint(0, total_bigrams)
        elif i + 1 == average_length:
            while frequency_map[curr_bigram_pos][0] != res[-1] or (not word_end(frequency_map[curr_bigram_pos])):
                curr_bigram_pos = random.randint(0, total_bigrams)
            '''while (not word_end(frequency_map[curr_bigram_pos])) and frequency_map[curr_bigram_pos][0] != res[-1]:
                curr_bigram_pos = random.randint(0, total_bigrams)'''
        else:
            while frequency_map[curr_bigram_pos][0] != res[-1] or terminating(frequency_map[curr_bigram_pos]):
                curr_bigram_pos = random.randint(0, total_bigrams)
            
        #print(f"Debug {frequency_map[curr_bigram_pos]}")
        #print(f"terminating({frequency_map[curr_bigram_pos]}) = {terminating(frequency_map[curr_bigram_pos])}")
        res += frequency_map[curr_bigram_pos][1]
    return res

def terminating(bigram):
    return word_start(bigram) or word_end(bigram)
def word_start(bigram):
    return bigram[0] == terminator
def word_end(bigram):
    return bigram[1] == terminator

if __name__=="__main__":
    main()
