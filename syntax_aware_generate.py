
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