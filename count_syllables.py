
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
 
    word = word.lower()
 
    # exception_add are words that need extra syllables
    # exception_del are words that need less syllables
 
    exception_add = ['serious','crucial']
    exception_del = ['fortunately','unfortunately']
 
    co_one = ['cool','coach','coat','coal','count','coin','coarse','coup','coif','cook','coign','coiffe','coof','court']
    co_two = ['coapt','coed','coinci']
 
    pre_one = ['preach']
 
    syls = 0 #added syllable number
    disc = 0 #discarded syllable number
 
    #1) if letters < 3 : return 1
    if len(word) <= 3 :
        syls = 1
        return syls
 
    #2) if doesn't end with "ted" or "tes" or "ses" or "ied" or "ies", discard "es" and "ed" at the end.