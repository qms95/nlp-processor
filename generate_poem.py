
import codecs
import nltk
import random
import re
import string
import csv
import inflect
from count_syllables import count_syllables


class PoemGenerator(object):
    def __init__(self, corpus='buzzfeed_facebook_statues.csv'):
        self.only_punctuation = re.compile(r'[^\w\s]+$')
        self.spaces_and_punctuation = re.compile(r"[\w']+|[.,!?;]")
        self.sents = []
        self.words = []
        self.all_words = []
        self.inflect_engine = inflect.engine()
        self.read_corpus(corpus)
        self.bigrams = list(nltk.bigrams(self.words))