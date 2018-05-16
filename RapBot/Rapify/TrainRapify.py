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
import win32com.client as wincl

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


def read_file(file_name='collection.json', language='en'):
    # TODO finish query
    file = os.getcwd() + '/../Lyrics/' + '_' + language + "/" + file_name
    speak = wincl.Dispatch("SAPI.SpVoice")
    with open(file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        artist_count = 0
        song_count = 0
        for song in data["songs"]:
                print(song)
                speak.Speak(data["songs"][song]["lyrics"])
                song_count += 1
        print("total artists scraped: " + str(artist_count))
        print("total songs scraped " +str(song_count))
        # for artist in data['artists']:
        #     print(artist)
        #     for song in (data['artists'][artist]['songs']):
        #         print('---' + song + '---')
        #         print(data['artists'][artist]['songs'][song]['lyrics'])


# ---------------CODE--------------------
read_file(file_name='Hef.json', language='nl')
