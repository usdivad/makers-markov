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
filename = 'txt/knausgaard.txt'
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
MARKOV_ORDER = 2
sentence = []

# Makes certain assumptions about the length of the text file
offset = 0
original_idx = 0
continue_original = True
valid_beginning = False

# # Simple, no begin/end checks
# offset = randint(0, len(words)/2)
# for i in xrange(SENTENCE_LENGTH):
#     idx = offset+i
#     sentence.append(words[idx])

# With begin/end checks
while not valid_beginning:
    offset = randint(0, len(words)/2)
    original_idx = offset
    word = words[original_idx]
    # if strf.is_string_beginning(word):
    if strf.is_string_beginning(word):
        valid_beginning = True
        # sentence.append(word)
        # print word + ' is a valid beginning'

while continue_original:
    # print 'idx: {}, offset: {}, max: {}'.format(str(original_idx), str(offset), str(offset+SENTENCE_LENGTH))
    word = words[original_idx]
    if word != '' and word != ' ':
        sentence.append(word)
    original_idx += 1
    if original_idx >= offset+SENTENCE_LENGTH:
        try:
            if strf.is_string_end(word[-1]):
                # print word + ' is ending'
                # print 'DONE'
                continue_original = False
            # else:
            #     print word + ' is not a phrase end'
        except:
            print 'ran to the end of the file!'
            break
    # original_idx += 1

sentence = strf.format_text(sentence)
# sentence = strf.format_bible(sentence)

sentence_str = ' '.join(sentence)

print ''
print 'SUBSEQUENCE FROM ORIGINAL:'
print sentence_str
print ''

# Generation: random
sentence = []
for i in xrange(SENTENCE_LENGTH):
    w = randint(0, len(words)-1)
    # print len(words)
    # print w
    sentence.append(words[w])
sentence = strf.format_text(sentence)

print ''
print 'RANDOM GENERATION:'
print ' '.join(sentence)
print ''

# Generation: markov
sentence = []
matrix = mm.transition_matrix(words, MARKOV_ORDER)

# # Print the transition matrix
# for k in mm.to_probabilities(matrix):
#     # if len(matrix[k]) > 0:
#     print '{}: {}'.format(str(k), str(matrix[k]))

# Sentence creation
sentence = mm.chain(matrix, SENTENCE_LENGTH, is_sequence_beginning=strf.is_string_beginning, is_sequence_end=strf.is_string_end)
# sentence = mm.chain(matrix, SENTENCE_LENGTH, is_sequence_beginning=strf.is_string_beginning, is_sequence_end=strf.is_string_end)
# sentence = mm.chain(matrix, SENTENCE_LENGTH)
sentence = strf.format_text(sentence)
# sentence = strf.format_bible(sentence)
# sentence = strf.format_script(sentence)

sentence_str = ' '.join(sentence)

print 'MARKOV GENERATION:'
print sentence_str
print ''


jiesu = time()
print 'Done in {} seconds'.format(str(jiesu-kaishi))