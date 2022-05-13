# Converts a json twitter dump to raw text file.
import codecs
import json
import sys


def get_text_from_json(filename):
    wi