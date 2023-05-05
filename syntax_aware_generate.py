
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
    print(replaced_tree)


def list_to_string(l):
    return str(l).replace(" ", "").replace("'", "")


def syntax_signature(tree, save=False):
    return list_to_string(syntax_signature_recurse(tree, save=save))


def syntax_signature_recurse(tree, save=False):
    global syntaxes
    if type(tree) is Tree:
        label = tree.label()
        if label == ',':
            label = 'COMMA'
        children = [syntax_signature_recurse(child, save=save) for child in tree if type(child) is Tree]
        if not children:
            if save:
                syntaxes[label].add(tree)
            return label
        else:
            if save:
                syntaxes[list_to_string([label, children])].add(tree)
            return [label, children]
    else:
        raise ValueError('Not a nltk.tree.Tree: {}'.format(tree))


def tree_replace(tree, cfds, preceding_children=[]):
    condition_search = ' '.join([' '.join(child.leaves()) for child in preceding_children]).lower()
    sig = syntax_signature(tree)
    if sig in syntaxes:
        matching_fragments = tuple(syntaxes[sig])
        if len(matching_fragments) > 1 and condition_search:
            matching_leaves = [' '.join(frag.leaves()) for frag in matching_fragments]
            most_common = get_most_common(condition_search, cfds)
            candidates = list(set(matching_leaves).intersection(set(most_common)))