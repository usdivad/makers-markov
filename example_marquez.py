'''
    Main executable!
'''

from random import randint
import re
from time import time

import makersmarkov as mm
import strf

# Timing
kaishi = time()


# TESTS
# Parse input into word array and frequency dict
# filename = 'txt/knausgaard.txt'
# filename = 'txt/joyce.txt'
filename = 'txt/marquez.txt'
word_freqs = {}
words = []
total_words = 0
with open(filename, 'r') as f:
    for line in f:
        line_words = re.split('\s+', line)
        # line_words = re.split('\s+\w+\s+', line) #trying with charsize = 2
        for word in line_words:
            total_words += 1
            words.append(word)
            if word in word_freqs:
                word_freqs[word] += 1
            else:
                word_freqs[word] = 1

# Generation
SENTENCE_LENGTH = 100
NUM_SENTENCES = 100
MARKOV_ORDER = 3
sentence = []
sentences = []

for i in xrange(NUM_SENTENCES):
    # Generation: markov
    sentence = []
    matrix = mm.transition_matrix(words, MARKOV_ORDER)

    # # Print the transition matrix
    # for k in mm.to_probabilities(matrix):
    #     # if len(matrix[k]) > 0:
    #     print '{}: {}'.format(str(k), str(matrix[k]))

    # Sentence creation
    sentence = mm.chain(matrix, SENTENCE_LENGTH, is_sequence_beginning=strf.is_string_beginning, is_sequence_end=strf.is_string_end)
    sentence = strf.format_text(sentence)

    sentence_str = ' '.join(sentence)
    sentences.append(sentence_str)

    # print 'MARKOV GENERATION:'
    # print sentence_str
    # print ''

    print 'Iteration #{} done'.format(str(i+1))

with open('marquez_out.txt', 'w') as f:
    for s in sentences:
        f.write(s + '\n\n')

jiesu = time()
print 'Done in {} seconds'.format(str(jiesu-kaishi))