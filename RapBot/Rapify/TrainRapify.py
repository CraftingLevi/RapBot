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
import json
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
    file = os.getcwd() + '/../Lyrics/compressed_scraped_lyrics.json'
    n = 0
    with open(file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for artist in data['artists']:
            print(artist)
            for song in (data['artists'][artist]):
                print('---' + song + '---')
                print(data['artists'][artist][song]['lyrics'])

# ---------------CODE--------------------
read_file('Afrika Bambaataa')
