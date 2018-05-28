"""
Written by Levi van der Heijden
Original Github Repository: -
PURPOSE: -
DESCRIPTION: -
REQUIRES: -
USEFUL: -
Last Updated: 11-05-2018
"""
import gensim
import spacy

import json
import os
import re

from gensim import corpora
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
            for token in sentence:
                token = token.text.lower()
                if token in ngram:
                    ngram[token] = ngram.get(token) + 1
                else:
                    ngram[token] = 1
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




def generate_word2vec_model(file_name = 'collection.json', language = 'nl'):
    file = os.getcwd() + '/../Lyrics/' + '_' + language + '/' + file_name
    file = open(file, 'r', encoding='utf-8')
    data = json.load(file)
    sentences = []
    for artist in data['artists']:
        for song in data['artists'][artist]['songs']:
            lyrics = data['artists'][artist]["songs"][song]['lyrics']
            for sentence in lyrics.split('\n'):
                sentences.append(gensim.utils.simple_preprocess(sentence))
    model = gensim.models.Word2Vec(
        sentences,
        size = 150,
        window = 10,
        min_count=2,
        workers=10
    )
    model.train(sentences, total_examples=len(sentences), epochs=10)
    model.save(os.getcwd() + '/../Rapify/' + 'testword2vecmodel')

def generate_LDA_model(file_name = 'collection.json', language = 'nl'):
    file = os.getcwd() + '/../Lyrics/' + '_' + language + '/' + file_name
    file = open(file, 'r', encoding='utf-8')
    data = json.load(file)
    sentences = []
    STOP_WORDS = load_stopwords()
    if language == 'nl':
        nlp = spacy.load('nl_core_news_sm')
    elif language == 'en':
        nlp = spacy.load('en_core_web_lg')
    else:
        print("language '" + language + "' not supported")
    for artist in data['artists']:
        print(artist)
        for song in data['artists'][artist]['songs']:
            lyrics = data['artists'][artist]["songs"][song]['lyrics']
            for sentence in lyrics.split('\n'):
                s = ''
                nlpdata = nlp(sentence)
                for token in nlpdata:
                    if token.text.lower() not in STOP_WORDS and token.pos_ in ['NOUN', 'ADJ', 'VERB', 'ADV']:
                        s = s + token.text + " "
                s.strip()
                sentences.append(gensim.utils.simple_preprocess(s))
    print('I will now create the LDA model')
    dictionary = corpora.Dictionary(sentences)
    doc_term_matrix = [dictionary.doc2bow(sentence) for sentence in sentences]
    Lda = gensim.models.ldamodel.LdaModel
    ldamodel = Lda(doc_term_matrix, num_topics=5, id2word=dictionary, passes=300)
    ldamodel.save(os.getcwd() + '/../Rapify/' + 'testldamodel')

def load_stopwords():
    STOP_WORDS = []
    file = os.getcwd() + '/../STOP_WORDS'
    file = open(file, 'r', encoding='utf-8')
    for word in file.readlines():
        STOP_WORDS.append(word.replace('\n', ''))
    return STOP_WORDS

def display_topics(model_path=os.getcwd() + '/../Rapify/testldamodel'):
    model = gensim.models.LdaModel.load(model_path)
    for topic in model.show_topics():
        for word in topic:
            print(word)
# ---------------CODE--------------------
# read_file(file_name='Adje.json', language='nl')
# print(findSlang())
#createRhymeScheme()
#testing_word2vec()
#generate_LDA_model()
display_topics()
