'''

Higher-order Markov chain implementation

'''
from random import choice


# Create a pseudo transition matrix (actually nested dicts) from list data and int order.
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


def truth(x):
    return True

# Run the Markov chain process to generate an output list
def chain(transition_matrix, size, is_sequence_beginning=truth, is_sequence_end=truth):
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
        # print cur_state
        if is_sequence_beginning(cur_state):
            valid_state = True
        # print 'retrying beginning'
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
        if idx >= size and is_sequence_end(cur_state[-1]):
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
