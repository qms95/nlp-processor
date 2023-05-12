
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