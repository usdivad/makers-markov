'''
    String formatting
'''

import re

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
            # re_punctuation = re.compile(r'\.|\?|\!')
            re_punctuation = re.compile(r'\W$')
            if prev_word != '' and re.match(re_punctuation, prev_word) != None:
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

# Movie script formatting
# add newlines after
def format_script(formatted_result_arr):
    script_result_arr = []
    prev_word = ''
    for i in xrange(len(formatted_result_arr)):
        cur_word = formatted_result_arr[i]
        # End of CAPPED PHRASE
        if len(prev_word) > 1 and prev_word.upper() == prev_word and re.match('\W$', prev_word) == None and cur_word.upper() != cur_word:
            print 'end capped: prev is {} and cur is {}'.format(prev_word, cur_word)
            cur_word = '\n' + cur_word.title()
        # Beginning of CAPPED PHRASE
        elif (len(prev_word) <= 1 or (prev_word.upper() != prev_word and re.match('\d', prev_word) != None)) and re.match('\W', prev_word) != None and cur_word.upper() == cur_word:
            print 'begin capped: prev is {} and cur is {}'.format(prev_word, cur_word)
            cur_word = '\n\n' + cur_word 
        script_result_arr.append(cur_word)
        prev_word = cur_word
    return script_result_arr


# Check for end of phrase: only takes into account .?!
def is_string_end(s):
    if len(s) > 0 and re.match('\.|\?|\!', s[-1]) != None:
        return True
    else:
        return False

# Check for beginning of phrase: caps, numbers, non-words
def is_string_beginning(s):
    if len(s) > 0 and s != ' ' and re.match('^[A-Z0-9\W]', s[0]) != None:
        return True
    else:
        return False