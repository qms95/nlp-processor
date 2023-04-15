
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