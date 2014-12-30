import random

'''

data arr

'''
def transition_matrix(data, order):

    matrix = {}
    length = len(data)

    # Initialize array representation of current state
    # e.g. ['g','a','t','c','t']
    cur_state = []
    for i in xrange(order):
        cur_state.append('')

    # Feed data into matrix
    # format: {(a,b,c): {'b': 0.4, 'a': 0.6}}
    for state_new in data:
        state_key = tuple(cur_state)
        if state_key in matrix:
            state_matrix = matrix[state_key]
            if state_new in state_matrix:
                state_matrix[state_new] += 1
            else:
                state_matrix[state_new] = 1
        else:
            matrix[state_key] = {}

        cur_state = cur_state[1:]
        cur_state.append(state_new)
        # print cur_state

    return matrix


# Parse input into word array and frequency dict
filename = 'knausgaard.txt'
word_freqs = {}
words = []
total_words = 0
with open(filename, 'r') as f:
    for line in f:
        line_words = line.split(' ')
        for word in line_words:
            total_words += 1
            words.append(word)
            if word in word_freqs:
                word_freqs[word] += 1
            else:
                word_freqs[word] = 1

# Generation: random
SENTENCE_LENGTH = 100
sentence = []
for i in xrange(SENTENCE_LENGTH):
    w = random.randint(0, len(words))
    sentence.append(words[w])

print ' '.join(sentence)


# Generation: markov
matrix = transition_matrix(words, 2)
for k in matrix:
    if len(matrix[k]) > 0:
        print '{}: {}'.format(str(k), str(matrix[k]))