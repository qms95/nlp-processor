# Converts a json twitter dump to raw text file.
import codecs
import json
import sys


def get_text_from_json(filename):
    with codecs.open(filename, 'r', 'utf-8') as f:
        return [item['text'] for item in json.loads(f.read())]


def