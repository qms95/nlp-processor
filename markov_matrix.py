
"""
My idea here is to encode the entire corpus as one giant two-dimensional numpy array of floats where each row is a
condition word and each column in that row is every other word in the corpus and the probability that the word follows
the conditional word.

This was an interesting idea, but ultimately not that useful since the resulting numpy array is significantly larger
than just storing the CFD in a python dictionary. There might be some crazy linear algebra I could run to compress this
array to make it less sparse. But, I would need to use the same N words for all corpora and I think that the resulting
compressed arrays would only be really useful for comparing with each other to find things like "closeness" between two
corpora as defined by the probabilities that some words follow other words in the text. Also, using the same N words
across all corpora is less awesome because you will miss out on the unique words (names, proper nouns, etc.) present in
only some corpora.
"""
import codecs
import sys