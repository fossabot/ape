import nltk


# All resources for NLTK are at
# http://nltk.org/nltk_data/

# print(nltk.corpus.words.words()[:20])
# print(nltk.corpus.stopwords.words("english"))

# Removing stop words
# From alice

alice = nltk.corpus.gutenberg.words("carroll-alice.txt")
alice = [word.lower() for word in alice if word.isalpha()]
alice_fd = nltk.FreqDist(alice)

alice_100 = alice_fd.most_common(100)
common = [word[0] for word in alice_100]
print(common)
descriptive = set(common) - set(nltk.corpus.stopwords.words())
print(descriptive)
