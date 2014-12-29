import random
# def markov_chain(data, order):

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