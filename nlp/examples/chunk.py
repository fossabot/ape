import nltk

text = 'I want to be at the coffee shop in New York after I get off the jet plane. What about movie tonight?'

text_tag = nltk.pos_tag(nltk.word_tokenize(text))
print(text_tag)

sequence = '''
              Chunk:
                {<NNPS>+}
                {<NNP>+}
                {<NN>+}
            '''

NPchunker = nltk.RegexpParser(sequence)
result = NPchunker.parse(text_tag)
print(result)
