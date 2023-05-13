
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
    for text in load_text_files(dirname):
        full_text += text
    return nlp(full_text)


def load_object_to_file(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)


def save_object_to_file(filename, object):
    with open(filename, 'wb') as f:
        pickle.dump(object, f)


def build_content_dict(content_syntax):
    content_dict = {}
    for word in content_syntax:
        if word.tag not in content_dict:
            content_dict[word.tag] = {}
        if word.dep not in content_dict[word.tag]:
            content_dict[word.tag][word.dep] = set()
        content_dict[word.tag][word.dep].add(word)
    return content_dict


def find_closest_content_word(template_word, content_dict):
    closest = None
    closest_score = 0.0

    if template_word.tag in content_dict:
        if template_word.dep in content_dict[template_word.tag]:
            content_word_set = content_dict[template_word.tag][template_word.dep]