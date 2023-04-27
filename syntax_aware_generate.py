
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
                    parsed = parser.parse(sent)
                except TypeError:
                    pass
                syntax_signature(parsed, save=True)
        with open(SYNTAXES_FILE, 'wb+') as pickle_file:
            pickle.dump(syntaxes, pickle_file)
    else:
        with open(SYNTAXES_FILE, 'rb+') as pickle_file:
            syntaxes = pickle.load(pickle_file)

    if not os.path.exists(CFDS_FILE):
        with codecs.open(filename, encoding='utf-8') as corpus:
            cfds = [make_cfd(corpus.read(), i, exclude_punctuation=False, case_insensitive=True) for i in range(2, 5)]
            with open(CFDS_FILE, 'wb+') as pickle_file:
                pickle.dump(cfds, pickle_file)
    else:
        with open(CFDS_FILE, 'rb+') as pickle_file:
            cfds = pickle.load(pickle_file)

    sents = nltk.corpus.gutenberg.sents('austen-emma.txt')
    if word_limit:
        sents = [sent for sent in sents if len(sent) < word_limit]
    sent = random.choice(sents)
    parsed = parser.parse(' '.join(sent))
    print(parsed)
    print(' '.join(parsed.leaves()))
    replaced_tree = tree_replace(parsed, cfds, [])
    print('=' * 30)
    print(' '.join(replaced_tree.leaves()))