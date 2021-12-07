
import re
import string
from nltk.corpus import cmudict


cmu = cmudict.dict()


def count_syllables(word):