"""
Written by Levi van der Heijden
Original Github Repository: -
PURPOSE: -
DESCRIPTION: -
REQUIRES: -
USEFUL: -
Last Updated: 11-05-2018
"""

import spacy

import json
import os
import re
from nltk import ngrams as ng

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
    if language == 'nl':
        nlp = spacy.load('nl_core_news_sm')
    elif language == 'en':
        nlp = spacy.load('en_core_web_lg')
    else:
        print("language '" + language + "' not supported")
    with open(file, 'r', encoding='utf-8') as file:
        data = json.load(file)
        artist_count = 0
        song_count = 0
        word_count = 0
        for artist in data["artists"]:
            artist_count += 1
            print(artist_count)
            for song in data["artists"][artist]["songs"]:
                song_count += 1
                lyrics = nlp(data["artists"][artist]["songs"][song]["lyrics"])
                for token in lyrics:
                    word_count += 1
        print("total artists scraped: " + str(artist_count))
        print("total songs scraped " + str(song_count))
        print("total words scraped " + str(word_count))
        # for artist in data['artists']:
        #     print(artist)
        #     for song in (data['artists'][artist]['songs']):
        #         print('---' + song + '---')
        #         print(data['artists'][artist]['songs'][song]['lyrics'])


def ngrams(file_name='Adje.json', language='nl', n=1, probabilities=True):
    file = os.getcwd() + '/../Lyrics/' + '_' + language + '/' + file_name
    file = open(file, 'r', encoding='utf-8')
    data = json.load(file)
    nlp = spacy.load('nl_core_news_sm')
    ngram = {}
    for song in data['songs']:
        lyrics = data["songs"][song]['lyrics']
        for sentence in lyrics.split('\n'):
            sentence = sentence
            sentence = nlp(sentence)
            ng(sentence)
            # for token in sentence:
            #     token = token.text.lower()
            #     if token in ngram:
            #         ngram[token] = ngram.get(token) + 1
            #     else:
            #         ngram[token] = 1
    print(ngram)
    print(len(ngram))


def findSlang(file_name='collection.json', language='en', n=1, probabilities=True):
    file = os.getcwd() + '/../Lyrics/' + '_' + language + '/' + file_name
    file = open(file, 'r', encoding='utf-8')
    data = json.load(file)
    if language == 'nl':
        nlp = spacy.load('nl_core_news_sm')
    elif language == 'en':
        nlp = spacy.load('en_core_web_lg')
    else:
        print('language (' + language + ') is not supported')
    ngram = {}
    for artist in data['artists']:
        print(artist)
        for song in data['artists'][artist]['songs']:
            lyrics = nlp(data['artists'][artist]["songs"][song]['lyrics'])
            for token in lyrics:
                if token.text not in nlp.vocab and not re.search('\n', token.text):
                    token = token.text.lower()
                    if token in ngram:
                        ngram[token] = ngram.get(token) + 1
                    else:
                        ngram[token] = 1
    top20 = [(k, ngram[k]) for k in sorted(ngram, key=ngram.get, reverse=True)][:20]
    return top20

def createRhymeScheme(file_name ='Adje.json', language='nl'):
    #TODO implement https://pdfs.semanticscholar.org/8b66/ea2b1fdc0d7df782545886930ddac0daa1de.pdf
    file = os.getcwd() + '/../Lyrics/' + '_' + language + '/' + file_name
    file = open(file, 'r', encoding='utf-8')
    data = json.load(file)
    if language == 'nl':
        nlp = spacy.load('nl_core_news_sm')
    elif language == 'en':
        nlp = spacy.load('en_core_web_lg')
    else:
        print('language (' + language + ') is not supported')
    for song in data['songs']:
        print('-----------' + song + '----------------')
        lyrics = data['songs'][song]['lyrics']
        sentences = []
        for sentence in lyrics.split('\n'):
            if sentence is not '':
                sentences.append(sentence)
                print(repr(sentence))
# ---------------CODE--------------------
# read_file(file_name='Adje.json', language='nl')
#print(findSlang())
createRhymeScheme()