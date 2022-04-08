
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
        with codecs.open(corpus, 'r', 'utf-8') as corpus_content:
            text = corpus_content.read()
            sents = nltk.tokenize.sent_tokenize(text)
            words = nltk.tokenize.word_tokenize(text)
            self.sents.extend(sents)
            self.words.extend(words)
            self.all_words.extend([word for word in words
                                   if not
                                   self.only_punctuation.match(word)])

    def read_csv_corpus(self, corpus):
        raise NotImplementedError('Haven\'t implemented generic csv reading')

    def read_buzzfeed_corpus(self, corpus):
        with open(corpus, newline='', encoding='utf-8') as statuses:
            reader = csv.reader(statuses, delimiter=',')
            for row in reader:
                if 'via buzzfeed ' not in row[1].lower():  # only English
                    # split title into a list of words and punctuation
                    title = self.spaces_and_punctuation.findall(row[2])
                    # spell out digits into ordinal words for syllable counting
                    title = [string.capwords(
                             self.inflect_engine.number_to_words(int(word)))
                             if word.isdigit() else word for word in title]
                    self.sents.append(title)
                    self.words.extend(title)
                    # all_words only contains words, no punctuation
                    self.all_words.extend([word for word in title
                                           if not
                                           self.only_punctuation.match(word)])

    def markov(self, word, n):
        if n > 0:
            print(word,)