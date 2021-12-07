
import re
import string
from nltk.corpus import cmudict


cmu = cmudict.dict()


def count_syllables(word):
    lower_word = word.lower()
    if lower_word in cmu:
        return max([len([y for y in x if y[-1] in string.digits])
                    for x in cmu[lower_word]])
    else:
        return sylco(word)
 

 # by M. Emre Aydin from http://eayd.in/?p=232
def sylco(word) :