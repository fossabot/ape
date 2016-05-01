import nltk

alice = nltk.corpus.gutenberg.words("carroll-alice.txt")

alice = alice[:1000]

alice_str = ' '.join(alice)
new_file = open('export_alice_1000.txt', 'w')
newfile.write(alice_str)
newfile.close()
