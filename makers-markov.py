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
    idx = 0
    continue_chain = True
    deadend_transitions = 0
    prev_deadend = True
    cur_deadend = []
    longest_deadend = []
    deadend_counts = []
    deadends = []
    valid_state = False
    
    # Prevent empty begin state (for strings only '')
    while not valid_state:
        cur_state = list(choice(list(transition_matrix.keys())))
        if is_phrase_beginning(cur_state):
            valid_state = True
        print 'retrying beginning'
    result_arr = cur_state[:]
    # print 'RESULT ARR: ' + str(result_arr)

    # Chainin'
    # for i in xrange(size-1):
    while continue_chain:
        next_state, is_deadend = choose_next(transition_matrix, cur_state)
        
        # Collecting stats about dead ends
        if is_deadend:
            deadend_transitions += 1
            cur_deadend.append(next_state)
            prev_deadend = True
        else:
            if len(cur_deadend) > len(longest_deadend):
                longest_deadend = cur_deadend
            deadend_counts.append(len(cur_deadend))
            deadends.append(' '.join(cur_deadend))
            cur_deadend = []
            prev_deadend = False

        result_arr.append(next_state)
        cur_state = cur_state[1:]
        cur_state.append(next_state) #update cur_state's last elm
        # print str(i) + ': cur_state is ' + str(cur_state)

        # See whether to continue or not
        idx += 1
        if idx >= size and is_phrase_end(cur_state[-1]):
            continue_chain = False
    
    # Stats about process
    if len(cur_deadend) > len(longest_deadend):
        longest_deadend = cur_deadend
        deadend_counts.append(len(cur_deadend))
    print 'MARKOV PROCESS STATS:'
    print '{} dead-end transitions out of {} states: {}%'.format(str(deadend_transitions), str(idx), str(100*float(deadend_transitions)/idx))
    print 'Dead-ends:\n\'' + ' ~~~ '.join(deadends) + '\''
    print 'Dead-end counts: ' + str(deadend_counts)
    print 'Longest consecutive dead-ends: {} ({})'.format(str(len(longest_deadend)), ' '.join(longest_deadend))
    print ''
    return result_arr

# Choose next state in transition matrix. Assumes matrix is NOT in probability-form
def choose_next(transition_matrix, state):
    deadend_transition = False
    cur_state = tuple(state)
    # print cur_state
    state_matrix = {}
    if cur_state not in transition_matrix or len(transition_matrix[cur_state]) < 1:
        # print 'WARNING: state {} is not in transition matrix'.format(str(cur_state))
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
            deadend_transition = True
            # print 'WARNING: state {} can only transition to \'{}\'. Try using a smaller Markov order'.format(str(cur_state), str(sk))
        for i in xrange(sv):
            # print 'sk is ' + sk
            weighted_state_arr.append(sk)
    # Choose a new state
    return (choice(weighted_state_arr), deadend_transition)

# Basic formatting for text output
def format_text(result_arr):
    prev_word = 'Nothing'
    cur_word = ''
    formatted_result_arr = []
    for i in xrange(len(result_arr)):
        # cur_word = re.sub(r'\s+', ' ', result_arr[i])
        # print result_arr[i] + ' vs ' + cur_word
        cur_word = result_arr[i]
        if cur_word != '':
            if prev_word != '' and re.match('\.|\?|\!', prev_word[-1]) != None:
                cur_word_arr = list(cur_word)
                if len(cur_word_arr) > 0:
                    cur_word_arr[0] = cur_word_arr[0].upper()
                    cur_word = ''.join(cur_word_arr)
            formatted_result_arr.append(cur_word)
            prev_word = cur_word

    formatted_result_arr[0] = formatted_result_arr[0].title()
    last_word = formatted_result_arr[-1]
    if len(last_word) > 0 and re.match('\.|\?|\!', last_word[-1]) == None:
        formatted_result_arr[-1] = last_word + '.'
    return formatted_result_arr

# Check for end of phrase: only takes into account .?!
def is_phrase_end(s):
    if len(s) > 0 and re.match('\.|\?|\!', s[-1]) != None:
        return True
    else:
        return False

# Check for beginning of phrase: caps, numbers, non-words
def is_phrase_beginning(s):
    if len(s) > 0 and re.match('^[A-Z0-9\W]', s[0]) != None:
        return True
    else:
        return False

# Special Bible formatting
# add newlines before numbers
def format_bible(formatted_result_arr):
    bible_result_arr = []
    for i in xrange(len(formatted_result_arr)):
        cur_word = formatted_result_arr[i]
        if re.match('^\d+', cur_word) != None:
            cur_word = '\n\n' + cur_word
        bible_result_arr.append(cur_word)
    return bible_result_arr

# TESTS

# Parse input into word array and frequency dict
# filename = 'txt/knausgaard.txt'
# filename = 'txt/joyce.txt'
filename = 'txt/kingjames.txt'
word_freqs = {}
words = []
total_words = 0
with open(filename, 'r') as f:
    for line in f:
        line_words = re.split('\s+', line)
        for word in line_words:
            total_words += 1
            words.append(word)
            if word in word_freqs:
                word_freqs[word] += 1
            else:
                word_freqs[word] = 1

# Generation
SENTENCE_LENGTH = 100
MARKOV_ORDER = 2
sentence = []

# Generation: random
for i in xrange(SENTENCE_LENGTH):
    w = randint(0, len(words)-1)
    # print len(words)
    # print w
    sentence.append(words[w])
sentence = format_text(sentence)
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
sentence = format_text(sentence)
sentence = format_bible(sentence)
print 'MARKOV GENERATION:'
print ' '.join(sentence)
print ''