###########################################
########## NLTK  Usage demonstration ######
###########################################

# Author: Sai Uday Shankar Korlimarla
# Email: skorlimarla@unomaha.edu

import nltk
from nltk.corpus import inaugural
import pandas as pd
import re


print("Abbreviations")
print(nltk.help.upenn_tagset())

print("Gutenberg Ids:\n{}".format(nltk.corpus.gutenberg.fileids()))

md = nltk.corpus.gutenberg.words("melville-moby_dick.txt")

print(md[:8])
print("Length of book {}".format(len(md)))
print("Boat: {}".format(md.count('boat')))

md_set = set(md)
print("Unique by set: {}".format(len(md_set)))

print("Average by words: {}".format(len(md)/len(md_set)))


md_sents = nltk.corpus.gutenberg.sents("melville-moby_dick.txt")
print("Average by words per sentence: {}".format(len(md)/len(md_sents)))

print("inaugral Ids:\n{}".format(inaugural.fileids()))

for speech in inaugural.fileids():
    words_total = len(inaugural.words(speech))
    print("Speech: {0} has total words: {1}".format(speech, words_total))

speech_len = [(len(inaugural.words(speech)), speech) for speech in inaugural.fileids()]
print("Biggest Speech: {}".format(max(speech_len)))
print("shortest Speech: {}".format(min(speech_len)))

for speech in inaugural.fileids():
    words_total = len(inaugural.words(speech))
    sentence_total = len(inaugural.sents(speech))
    print("Sentence average: {}".format(words_total/sentence_total))

data = pd.DataFrame([int(speech[:4]), len(inaugural.words(speech))/len(inaugural.sents(speech))] for speech in inaugural.fileids())
data.columns = ['year', 'Average WPS']
fig = data.plot("year", figsize=(15,5)).get_figure()
# File inaugural.png is saved on the disk - same location as this code
fig.savefig('inaugural.png')

# data.head(10)
# data.columns = ["Year", "Average WPS"]

alice = nltk.corpus.gutenberg.words("carroll-alice.txt")
alice_fd = nltk.FreqDist(alice)

print("Rabbit: {}".format(alice_fd["Rabbit"]))
print("Most Common: {}".format(alice_fd.most_common(5)))

# Words used only once - It's called hapaxes
print("Words Used Once: {}".format(alice_fd.hapaxes()))

# Conditional Frequency distribution
names = [("Group A", "Paul"), ("Group A", "Mike"), ("Group A", "Katy"), ("Group B", "Amy"), ("Group B", "Joe"), ("Group B", "Amy")]

# Regular & Conditional Frequency distribution

print(nltk.FreqDist(names))
print(nltk.ConditionalFreqDist(names))
for each in nltk.FreqDist(names):
    print each
for each in nltk.ConditionalFreqDist(names):
    print each


# Remove most common words
alice = nltk.corpus.gutenberg.words("carroll-alice.txt")
# FreqDist
alice_fd = nltk.FreqDist(alice)
# FreqDist then common 100
alice_fd_100 = alice_fd.most_common(100)
# Save word only - for comparision
alice_100 = [word[0] for word in alice_fd_100]

moby = nltk.corpus.gutenberg.words("melville-moby_dick.txt")
# FreqDist
moby_fd = nltk.FreqDist(moby)
# FreqDist then common 100
moby_fd_100 = moby_fd.most_common(100)
# Save word only - for comparision
moby_100 = [word[0] for word in moby_fd_100]

# This is elementary
print(set(alice_100) - set(moby_100))
print(set(moby_100) - set(alice_100))

# Tokenize text
text1 = "I think it might rain today."
tokens = nltk.word_tokenize(text1)
print(tokens)

# Bi-Grams
bigrams = nltk.bigrams(tokens)

for item in bigrams:
    print item

# Trigrams
trigrams = nltk.trigrams(tokens)

for item in trigrams:
    print item

# n-grams
from nltk.util import ngrams
text2 = "If it is noce outside, I will go to the beach"

# Using ngrams from nltk.util

tokens = nltk.word_tokenize(text2)
bigrams = ngrams(tokens,2)
trigrams = ngrams(tokens,3)
fourgrams = ngrams(tokens, 4)

def n_grams(text,n):
    tokens = nltk.word_tokenize(text)
    grams = ngrams(tokens, n)
    return grams

text3 = text1 + " " + text2
fourgrams = n_grams(text2, 4)

for item in fourgrams:
    print item


##########################################
########## REGEX and NLTK ################
##########################################

# Basic
'''
^  Start of string
$ End of string
. Wild card character
[chr] Match one character
[a-m] Matches one character in range
'''

# usage of basic- examples
'''
^...$ - All three letter words
c..$ - Words starting with c
^c  - Open ended -anything starting with c
ing$ - Any word with ing as the last three letters
^[chr]at$ - cat har or rat
'''
# More
'''
    ? - Previous character occurs 0 or 1 times
    * - Previous character occurs 0 or more times
    + - Previous character occurs 1 or more time
    a|e - Matches one or the other
    () - Parenthesis rouping for expressions
    \ - Escape character
'''
# email ending with .com
'''
^.+@.+\.com$
'''


alice = nltk.corpus.gutenberg.words("carroll-alice.txt")
print(set([word for word in alice if re.search("^new", word)]))
print(set([word for word in alice if re.search("ful$", word)]))
print(set([word for word in alice if re.search("^..nn..$", word)]))
print(set([word for word in alice if re.search("^[chr]at$", word)]))
print(set([word for word in alice if re.search("^.*nn.*$", word)]))
print(set([word for word in alice if re.search("^[aeiou]c.+y$", word)]))


#######################################
########### Tokenization ##############
########### Tagging ###################
########### Chunking ##################
#######################################

# Tokenization
my_text = "I am learning natural language processing"
tokens = nltk.word_tokenize(my_text)
print("Tokens:\n{}".format(tokens))
phrase = "I am learning natural language processing. I am learning to tokenize"
tokens_sent = nltk.sent_tokenize(phrase)
print("Sentence Tokens:\n{}".format(tokens_sent))
print("Breaking down further")
for item in tokens_sent:
    print(nltk.word_tokenize(item))

# Normalizing
moby = nltk.corpus.gutenberg.words("melville-moby_dick.txt")
moby_22 = moby[:22]
print(moby_22)

for word in moby_22:
    if word.isalpha():
        print word
        print word.lower()

# Doing the same - with comprehensions
moby_norm_22 = [word.lower() for word in moby_22 if word.isalpha()]
print("Norm:\n{}".format(moby_norm_22))

# Stemmers
############## Porter
porter = nltk.PorterStemmer()
my_list = ["cat", "cats", "dog", "dogs", "dawgs", "running", "city", "cities", "monday", "month", "monthly", "run"]

for word in my_list:
    print porter.stem(word)

lancaster = nltk.LancasterStemmer()
lancaster_list = [lancaster.stem(word) for word in my_list]
print(lancaster_list)
# Lancaster seems to work much better than porter

# Lemmatization - Better results but more computationally intensive
wnetlemma = nltk.WordNetLemmatizer()
for word in my_list:
    print wnetlemma.lemmatize(word)

# Parts of speech

text = "I walked to the cafe to buy coffee for work."
tokens = nltk.word_tokenize(text)
print("Parts of Phrase: {}".format(nltk.pos_tag(tokens)))
print(nltk.pos_tag(nltk.word_tokenize("I am going to watch Game of Thrones Season 6 Episode 2 today at 8 PM")))


moby_norm = [word.lower() for word in moby if word.isalpha()]
moby_tags = nltk.pos_tag(moby_norm, tagset="universal")

moby_nouns = [word for word in moby_tags if word[1] == "NOUN"]
moby_nouns_fd = nltk.FreqDist(moby_nouns)

# A description of moby dick
print(moby_nouns_fd.most_common(10))

# Multiple POS
# With conditional Frequency distribution

alice = nltk.corpus.gutenberg.words("carroll-alice.txt")
alice_norm = [word.lower() for word in alice if word.isalpha()]
alice_tags = nltk.pos_tag(alice_norm, tagset="universal")
alice_cfd = nltk.ConditionalFreqDist(alice_tags)

print(alice_cfd["over"])
print(alice_cfd["lower"])
for each in alice_cfd["answer"]:
    print each
