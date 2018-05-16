"""
Written by Levi van der Heijden
Original Github Repository: -
PURPOSE: -
DESCRIPTION: -
REQUIRES: -
USEFUL: -
Last Updated: 11-05-2018
"""
import ast
import base64

import os
import re

import requests
from nltk import tokenize as tok


BASE_URL = "http://api.genius.com"
file_path = os.getcwd() + "/../api_key_genius"
file = open(file_path, 'r', encoding='utf-8')
TOKEN = file.readline()
HEADERS = {'Authorization': "Bearer " + TOKEN}


# TODO implement http://anthology.aclweb.org/C/C14/C14-1059.pdf
# Fell, M., & Sporleder, C. (2014). Lyrics-based Analysis and classification of music.
# In Proceedings of COLING 2014, the 25th International Conference on Computational Linguistics:
# Technical Papers (pp. 620-631).



def generate_word_model():
    'do nothing'
    # TODO finish method stub


def read_file(artist):
    # TODO finish query
    dir = os.getcwd() + '/../Lyrics/' + artist + '/'
    n = 0
    for f in os.listdir(dir):
        with open(dir + f, 'r', encoding='utf-8') as file:
            if (n < 1):
                print(f)
                n += 1
                lyrics = file.readlines()
                for line in lyrics:
                    if line != '\n':
                        tokens = tok.word_tokenize(line)
                        print(tokens)

# ---------------CODE--------------------
# readFile('50 Cent')
