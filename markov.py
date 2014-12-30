from random import choice, randint
import re

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
    # format: {(a,b,c): {'b': 48, 'a': 69}}
    # "new_substate" is actually a "substate"
    for new_substate in data:
        # print 'cur_state: {}, new_substate: {}'.format(str(cur_state), str(new_substate))
        state_key = tuple(cur_state)
        if state_key in matrix:
            state_matrix = matrix[state_key]
            if new_substate in state_matrix:
                state_matrix[new_substate] += 1
            else:
                state_matrix[new_substate] = 1
        else:
            matrix[state_key] = {new_substate: 1}

        cur_state = cur_state[1:]
        cur_state.append(new_substate)
        # print cur_state

    return matrix

# Convert transition matrix to probabilities
def to_probabilities(matrix):
    new_matrix = {}
    for state in matrix:
        state_matrix = matrix[state]
        total_transitions = sum(state_matrix.values())
        for st in state_matrix:
            state_transition = float(state_matrix[st])
            prb = state_transition / total_transitions
            if state in new_matrix:
                new_matrix[state][st] = prb
            else:
                new_matrix[state] = {st: prb}
    return new_matrix

# Run the Markov chain process to generate an output list
def chain(transition_matrix, size):
    # cur_state = list(choice(list(transition_matrix.keys())))
    cur_state = []
    solo_transitions = 0
    # Prevent empty begin state (for strings only '')
    valid_state = False
    while not valid_state:
        cur_state = list(choice(list(transition_matrix.keys())))
        if not '' in cur_state:
            valid_state = True
    result_arr = cur_state[:]
    # print 'RESULT ARR: ' + str(result_arr)
    for i in xrange(size-1):
        next_state, solo = choose_next(transition_matrix, cur_state)
        if solo:
            solo_transitions += 1
        # print 'next state: ' + str(next_state)
        result_arr.append(next_state)
        # print result_arr
        cur_state = cur_state[1:]
        cur_state.append(next_state) #update cur_state's last elm
        print str(i) + ': cur_state is ' + str(cur_state)
    
    print '{} solo/dead-end transitions out of {} states: {}%'.format(str(solo_transitions), str(size), str(100*float(solo_transitions)/size))
    return result_arr

# Choose next state in transition matrix. Assumes matrix is NOT in probability-form
def choose_next(transition_matrix, state):
    solo_transition = False
    cur_state = tuple(state)
    # print cur_state
    state_matrix = {}
    if cur_state not in transition_matrix or len(transition_matrix[cur_state]) < 1:
        print 'WARNING: state {} is not in transition matrix'.format(str(cur_state))
        rand_state = choice(list(transition_matrix.keys()))
        state_matrix = transition_matrix[rand_state]
    else:
        state_matrix = transition_matrix[cur_state]

    # Create weighted state list
    # e.g. state matrix {a:2, b: 3} -> [a,a,b,b,b]
    weighted_state_arr = []
    for sk in state_matrix:
        sv = state_matrix[sk]
        if float(sv) / sum(state_matrix.values()) == 1:
            solo_transition = True
            print 'WARNING: state {} can only transition to \'{}\'. Try using a smaller MARKOV_ORDER'.format(str(cur_state), str(sk))
        for i in xrange(sv):
            # print 'sk is ' + sk
            weighted_state_arr.append(sk)
    # Choose a new state
    return (choice(weighted_state_arr), solo_transition)

def format_basic(result_arr):
    prev_word = ''
    cur_word = ''
    for i in xrange(len(result_arr)):
        cur_word = result_arr[i]
        if prev_word != '' and not re.match('\.|\?|\!', prev_word[-1]) == None:
            cur_word_arr = list(cur_word)
            cur_word_arr[0] = cur_word_arr[0].upper()
            cur_word = ''.join(cur_word_arr)
            result_arr[i] = cur_word
        prev_word = cur_word

    result_arr[0] = result_arr[0].title()
    last_word = result_arr[-1]
    if re.match('\.|\?|\!', last_word[-1]) == None:
        result_arr[-1] = last_word + '.'
    return result_arr


# TESTS

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

# Generation
SENTENCE_LENGTH = 1000
MARKOV_ORDER = 2
sentence = []

# Generation: random
for i in xrange(SENTENCE_LENGTH):
    w = randint(0, len(words)-1)
    # print len(words)
    # print w
    sentence.append(words[w])
format_basic(sentence)
print ''
print 'RANDOM GENERATION:'
print ' '.join(sentence)
print ''

# Generation: markov
matrix = transition_matrix(words, MARKOV_ORDER)
# # Print the transition matrix
# for k in to_probabilities(matrix):
#     # if len(matrix[k]) > 0:
#     print '{}: {}'.format(str(k), str(matrix[k]))

# Sentence creation
sentence = chain(matrix, SENTENCE_LENGTH)
format_basic(sentence)
print 'MARKOV GENERATION:'
print ' '.join(sentence)
print ''