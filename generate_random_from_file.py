
import nltk
import random
import string
import sys


def main(text):
    bigrams = list(nltk.bigrams(
        [token for token in nltk.word_tokenize(text.decode('utf8'))
         if set(token).difference(set(string.punctuation))]))