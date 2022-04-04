
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
        self.cfd = nltk.ConditionalFreqDist(self.bigrams)
        self.history = []

    def read_corpus(self, corpus):
        """Given filename of corpus, populate words, all_words, and sents."""
        if corpus.endswith('.csv'):
            if 'buzzfeed_facebook_statuses' in corpus:
                return self.read_buzzfeed_corpus(corpus)
            else:
                return self.read_csv_corpus(corpus)
        elif corpus.endswith('.txt'):
            return self.read_txt_corpus(corpus)
        else:
            raise TypeError(('Unrecognized corpus file type: %s.' % corpus) +
                            '".txt" and ".csv" are only supported')

    def read_txt_corpus(self, corpus):