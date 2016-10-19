# Text - Commmon encoding is UTF-8

# (Source) UTF-8 -> UNICODE -> PROCESSING -> UTF-8 (rendering)
# (Source) ASCII -> UNICODE -> PROCESSING -> UTF-8 (rendering)

import nltk

dec_inp_text = open("dec-independence.txt").read().decode('utf-8')
dec_inp_tokens = nltk.word_tokenize(dec_inp_text)
dec_inp_fd = nltk.FreqDist(dec_inp_tokens)
