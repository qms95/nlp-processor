
import nltk
import operator
import os
import pickle
import random
import re
import codecs
import sys
from nltk.tree import Tree
from collections import defaultdict
from tqdm import tqdm
from stat_parser import Parser

syntaxes = defaultdict(set)
SYNTAXES_FILE = 'syntaxes.p'
CFDS_FILE = 'cfds.p'


def tree_hash(self):
    return hash(tuple(self.leaves()))


Tree.__hash__ = tree_hash


# NOTE: to me: I need to replace nltk parse and tokenization with spacy because it is much faster and less detailed
# which is actually a plus. The problem is that spacy does not create a syntax tree like nltk does. However, it does
# create a dependency tree, which might be good enough for splitting into chunks that can be swapped out between
# corpora. Shitty bus wifi makes it hard to download spacy data and look up the docs.


def generate(filename, word_limit=None):
    global syntaxes
    parser = Parser()
    if not os.path.exists(SYNTAXES_FILE):
        #  sents = nltk.corpus.gutenberg.sents('results.txt')
        # NOTE: results.txt is a big file of raw text not included in source control, provide your own corpus.
        with codecs.open(filename, encoding='utf-8') as corpus:
            sents = nltk.sent_tokenize(corpus.read())
            if word_limit:
                sents = [sent for sent in sents if len(sent) < word_limit]
            sent_limit = min(1500, len(sents))
            sents[0:sent_limit]
            for sent in tqdm(sents):
                try: