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
    # format: {(a,b,c): {'b': 48, 'a': 69}}
    # "new_substate" is actually a "substate"
    for new_substate in data:
        state_key = tuple(cur_state)
        if state_key in matrix:
            state_matrix = matrix[state_key]
            if new_substate in state_matrix:
                state_matrix[new_substate] += 1
            else:
                state_matrix[new_substate] = 1
        else:
            matrix[state_key] = {}

        cur_state = cur_state[1:]
        cur_state.append(new_substate)
        # print cur_state

    return matrix

# Convert transition matrix to probabilities
def to_probabilities(matrix):
    for state in matrix:
        state_matrix = matrix[state]
        total_transitions = sum(state_matrix.values())
        for st in state_matrix:
            state_transition = float(state_matrix[st])
            state_matrix[st] = state_transition / total_transitions
    return matrix

# Run the Markov chain process to generate an output list
def chain(transition_matrix, size):
    cur_state = list(random.choice(list(transition_matrix.keys())))
    result_arr = cur_state[-1:]
    for i in xrange(size):
        next_state = choose_next(transition_matrix, tuple(cur_state))
        # print next_state
        result_arr += next_state
        cur_state[-1] = next_state #update cur_state's last elm
    return result_arr

# Choose next state in transition matrix. Assumes matrix is NOT in probability-form
def choose_next(transition_matrix, state):
    # cur_state = list(state)
    cur_state = state
    # print cur_state
    if cur_state not in transition_matrix:
        # print 'Warning: state not in transition matrix'
        return random.choice(list(transition_matrix.keys()))
    else:
        state_matrix = transition_matrix[cur_state]
        if len(state_matrix) < 1: # no possible transitions
            return random.choice(list(transition_matrix.keys()))
        else:
            # Create weighted state list
            # e.g. state matrix {a:2, b: 3} -> [a,a,b,b,b]
            weighted_state_arr = []
            for sk in state_matrix:
                sv = state_matrix[sk]
                for i in xrange(sv):
                    weighted_state_arr.append(sk)
            # Choose a random new state
            return random.choice(weighted_state_arr)




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

print 'RANDOM GENERATION:'
print ' '.join(sentence)
print '\n'

# Generation: markov
matrix = transition_matrix(words, 10)
# Print the transition matrix
for k in matrix:
    if len(matrix[k]) > 0:
        print '{}: {}'.format(str(k), str(matrix[k]))

# Sentence creation
sentence = chain(matrix, 25)
print 'MARKOV GENERATION:'
print ' '.join(sentence)