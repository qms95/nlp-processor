
import codecs
import os
import pickle
import random

import spacy

TEMPLATE_CORPUS = 'austencorpus'
CONTENT_CORPUS = 'lovecraftcorpus'

print('Loading spaCy model... ', end='')
nlp = spacy.load('en_core_web_lg')
print('Done')


def load_text_files(dirname):
    for (dirpath, dirnames, filenames) in os.walk(dirname):
        for filename in filenames:
            with codecs.open(os.path.join(dirpath, filename),
                             encoding='utf-8') as f:
                yield f.read()


def load_syntax(dirname):
    full_text = ''