import nltk

# Wikipedia - World war -II intorduction
text = open("example.txt").read().decode('utf-8')

text_tag = nltk.pos_tag(nltk.word_tokenize(text))
text_ch = nltk.ne_chunk(text_tag)
print(text_ch)

for chunk in text_ch:
    if hasattr(chunk, 'label'):
        print(chunk.label(), " ".join(c[0] for c in chunk.leaves()))
