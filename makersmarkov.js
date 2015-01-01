function transition_matrix(data, order) {
    var matrix = {};
    var length = data.length;

    // Initialize array representation of current state
    // e.g. ['g','a','t','c','t']
    var cur_state = [];
    for (var i=0; i<order; i++) {
        cur_state.push('');
    }

    // Feed data into matrix
    // format: {(a,b,c): {'b': 48, 'a': 69}}
    // "new_substate" is actually a "substate"
    for (var i=0; i<data.length; i++) {
        var new_substate = data[i];
        console.log(new_substate);
        var state_key = cur_state.toString(); //use string instead of tuple
        if (state_key in matrix) {
            state_matrix = matrix[state_key];
            if (new_substate in state_matrix) {
                state_matrix[new_substate] += 1;
            }
            else {
                state_matrix[new_substate] = 1;
            }
        }
        else {
            matrix[state_key] = {};
            matrix[state_key][new_substate] = 1;
        }

        cur_state = cur_state.slice(1);
        cur_state.push(new_substate);
    }

    return matrix;
}


// TESTING
console.log(transition_matrix([1,2,1,3,1,4,2,3,1,2,3], 2));