
"""
My idea here is to encode the entire corpus as one giant two-dimensional numpy array of floats where each row is a
condition word and each column in that row is every other word in the corpus and the probability that the word follows
the conditional word.

This was an interesting idea, but ultimately not that useful since the resulting numpy array is significantly larger
than just storing the CFD in a python dictionary. There might be some crazy linear algebra I could run to compress this