import operator
import os
import re
import json
import spacy
import matplotlib.pyplot as plt


def check_the_rhyme(file_name='collection.json', language='nl', cutoff=1000):
    # TODO implement https://pdfs.semanticscholar.org/8b66/ea2b1fdc0d7df782545886930ddac0daa1de.pdf
    STOP_WORDS = load_stopwords()
    file = os.getcwd() + '/../Lyrics/' + '_' + language + '/' + file_name
    file = open(file, 'r', encoding='utf-8')
    data = json.load(file)
    if language == 'nl':
        nlp = spacy.load('nl_core_news_sm')
    elif language == 'en':
        nlp = spacy.load('en_core_web_lg')
    else:
        print('language (' + language + ') is not supported')
    rhym_dict = {}
    vocabulary_size_dict = {}
    how_long_still = 0
    for artist in data['artists']:
        how_long_still += 1
        print('done ' + str(how_long_still) + ' out of 80')
        line_count = 0
        vocabulary = []
        for song in data['artists'][artist]['songs']:
            if line_count >= cutoff:
                break
            lyrics = data['artists'][artist]['songs'][song]['lyrics']
            sentences = ''
            for sentence in lyrics.split('\n'):
                if sentence is not '':
                    sentences = sentences + ' ' + sentence
                    line_count += 1
                    if line_count >= cutoff:
                        break
            tokens = nlp(sentences)
            token_list = []
            rhyme_count = 0
            rijk_count = 0
            rhyme_list = []
            for token in tokens:
                if not re.search("\w*[.,\/#!$%\^&\*;:{}=\-_`~()']\w*", token.text):
                    token_list.append(token.text.lower())
            for i in range(0, len(token_list)):
                current_word = token_list[i]
                other_words = token_list[i + 1:i + 15]
                if current_word not in vocabulary:
                    vocabulary.append(current_word)
                for j in range(0, len(other_words)):
                    checked_word = other_words[j]
                    if checked_word != None and is_stopword(current_word, STOP_WORDS) == False \
                            and is_stopword(checked_word, STOP_WORDS) == False:
                        if is_rhyme(current_word, checked_word):
                            rhyme_count += 1
                            rhyme_list.append(current_word + '-' + checked_word)
                            break
            if artist in rhym_dict:
                rhym_dict[artist] = rhym_dict.get(artist) + rhyme_count
            else:
                rhym_dict[artist] = rhyme_count
        if line_count >= cutoff and artist in vocabulary_size_dict:
            vocabulary_size_dict[artist] = vocabulary_size_dict.get(artist) + len(vocabulary)
            break
        elif line_count >= cutoff:
            vocabulary_size_dict[artist] = len(vocabulary)
    true_rhym_dict = {}
    for artist in rhym_dict.keys():
        if artist in vocabulary_size_dict:
            true_rhym_dict[artist] = rhym_dict.get(artist)
    file.close()
    return true_rhym_dict, vocabulary_size_dict


# We do not use rijk rijm, as it is inferiour
def is_rhyme(w1, w2):
    if check_rijk_rijm(w1, w2):
        return False
    if check_eind_rijm(w1, w2) or check_begin_rijm(w1, w2) or check_klinker_rijm(w1, w2):
        return True
    else:
        return False


def check_rijk_rijm(word1, word2):
    word1 = word_equalizer_nl(word1)
    word2 = word_equalizer_nl(word2)
    if word1 == word2:
        return True
    else:
        return False


def check_begin_rijm(word1, word2):
    word1 = word_equalizer_nl(word1)
    word2 = word_equalizer_nl(word2)
    if word1[:2] == word2[:2] and check_rijk_rijm(word1, word2) == False:
        return True
    else:
        return False

def remove_last_consonants(word1, word2):
    length1 = len(word1)
    length2 = len(word2)
    for i in range(1, length1):
        if re.search('[aeiou]', word1[length1 - i]):
            word1 = word1[:len(word1) - i + 1]
            break
    for i in range(1, length2):
        if re.search('[aeiou]', word2[length2 - i]):
            word2 = word2[:len(word2) - i + 1]
            break
    return word1, word2

def remove_first_consonants(w1, w2):
    for i in range(0, len(w1)):
        if re.search('[aeiou]', w1[i]):
            w1 = w1[i:]
            break
    for i in range(0, len(w2)):
        if re.search('[aeiou]', w2[i]):
            w2 = w2[i:]
            break
    return w1, w2

def check_klinker_rijm(w1, w2):
    w1, w2 = remove_last_consonants(w1, w2)
    w1, w2 = remove_first_consonants(w1, w2)
    w1 = word_equalizer_nl(w1)
    w2 = word_equalizer_nl(w2)
    if w1[:1] == w2[:1] or w1[len(w1) - 1] == w2[len(w2) - 1]:
        return True
    else:
        return False


# This is a pretty simply phonetic equilizer

def word_equalizer_nl(word):
    # TODO integrate list of exceptions
    word = word.replace('d', 't')
    word = word.replace('cc', 'ss')
    word = word.replace('ci', 'si')
    word = word.replace('ce', 'se')
    word = word.replace('c', 'k')
    word = word.replace('que', 'ke')
    word = word.replace('qu', 'kw')
    word = word.replace('z', 's')
    word = word.replace('v', 'f')
    word = word.replace('au', 'ou')
    word = word.replace('th', 't')
    word = word.replace('x', 'ks')
    word = word.replace('y', 'i')  # the rule of y as 'ie' or 'i' is vague
    word = word.replace('oe', '!')
    word = word.replace('ee', '#')
    word = word.replace('en', 'e')
    word = word.replace('aa', '*')
    word = word.replace('ij', '?')
    word = word.replace('ei', '?')
    word = word.replace('ui', '+')

    return word


def check_eind_rijm(word1, word2):
    word1 = word_equalizer_nl(word1)
    word2 = word_equalizer_nl(word2)
    if len(word1) <= len(word2):
        n = 0
        adding = False
        for i in range(0, len(word2) - 1):
            checking = word1[n:]
            checked = word2[i:len(word2)]
            if len(word2) - i == len(word1):
                adding = True
            if adding:
                n += 1
            if checked == checking and check_rijk_rijm(word1, word2) == False:
                return True
        else:
            return False
    else:
        return check_eind_rijm(word2, word1)


def load_stopwords():
    STOP_WORDS = []
    file = os.getcwd() + '/../STOP_WORDS_DUTCH'
    file = open(file, 'r', encoding='utf-8')
    for word in file.readlines():
        STOP_WORDS.append(word.replace('\n', ''))
    file.close()
    return STOP_WORDS


def is_stopword(w, STOP_WORDS=None):
    if STOP_WORDS is None:
        STOP_WORDS = load_stopwords()
    if w in STOP_WORDS:
        return True
    else:
        return False



"""
this function calculates the average rhyme using our scraped dataset
INPUT: a .json file with artists and songs and lyrics a key for years
OUTPUT: three dictionaries, <count of songs per year>, <sum of vocabulary_size for all songs per year>, 
        <sum of rhyme count for all songs per year>
USED BY: plot_rhym_voc_yearly()
"""


# BUGFIX: I used break instead of continue..., this is fixed now
def check_the_rhyme_yearly(file_name='collection.json', language='nl'):
    total_songs = 0
    STOP_WORDS = load_stopwords()
    file = os.getcwd() + '/../Lyrics/' + '_' + language + '/' + file_name
    file = open(file, 'r', encoding='utf-8')
    data = json.load(file)
    file.close()
    if language == 'nl':
        nlp = spacy.load('nl_core_news_sm')
    elif language == 'en':
        nlp = spacy.load('en_core_web_lg')
    else:
        print('language (' + language + ') is not supported')
    rhym_dict = {}
    vocabulary_size_dict = {}
    song_count_dict = {}
    how_long_still = 0
    for artist in data['artists']:
        how_long_still += 1
        print('done ' + str(how_long_still) + ' out of 80 (' + artist + ')')
        for song in data['artists'][artist]['songs']:
            total_songs += 1
            year = data['artists'][artist]['songs'][song]['release_date']
            if year is None:
                continue
            else:
                year = year[:4]
            vocabulary = []
            rhyme_count = 0
            lyrics = data['artists'][artist]['songs'][song]['lyrics']
            sentences = ''
            word_count = 1
            for sentence in lyrics.split('\n'):
                if sentence is not '':
                    sentences = sentences + ' ' + sentence
            tokens = nlp(sentences)
            token_list = []
            for token in tokens:
                if not re.search("\w*[.,\/#!$%\^&\*;:{}=\-_`~()']\w*", token.text):
                    token_list.append(token.text.lower())
            for i in range(0, len(token_list)):
                current_word = token_list[i]
                other_words = token_list[i + 1:i + 15]
                if current_word not in vocabulary:
                    vocabulary.append(current_word)
                for j in range(0, len(other_words)):
                    checked_word = other_words[j]
                    if checked_word is not None and is_stopword(current_word, STOP_WORDS) is False \
                            and is_stopword(checked_word, STOP_WORDS) is False:
                        word_count += 1
                        if is_rhyme(current_word, checked_word):
                            rhyme_count += 1
                            break
            if year in rhym_dict:
                rhym_dict[year] = rhym_dict.get(year) + rhyme_count/word_count
            else:
                rhym_dict[year] = rhyme_count/word_count
            if year in vocabulary_size_dict:
                vocabulary_size_dict[year] = vocabulary_size_dict.get(year) + len(vocabulary)
            else:
                vocabulary_size_dict[year] = len(vocabulary)
            if year in song_count_dict:
                song_count_dict[year] = song_count_dict[year] + 1
            else:
                song_count_dict[year] = 1
    print(total_songs)
    return song_count_dict, vocabulary_size_dict, rhym_dict




def check_the_rhyme_avg(file_name='collection.json', language='nl', rhyme_cutoff=15, sample_cutoff=5):
    STOP_WORDS = load_stopwords()
    file = os.getcwd() + '/../Lyrics/' + '_' + language + '/' + file_name
    file = open(file, 'r', encoding='utf-8')
    data = json.load(file)
    if language == 'nl':
        nlp = spacy.load('nl_core_news_sm')
    elif language == 'en':
        nlp = spacy.load('en_core_web_lg')
    else:
        print('language (' + language + ') is not supported')
    rhym_dict = {}
    vocabulary_size_dict = {}
    song_count_dict = {}
    how_long_still = 0
    total_artists = len(data["artists"])
    for artist in data['artists']:
        how_long_still += 1
        print('done ' + str(how_long_still) + ' out of ' + str(total_artists))
        line_count = 0
        song_count = 0
        if len(data['artists'][artist]['songs']) > sample_cutoff:
            for song in data['artists'][artist]['songs']:
                vocabulary = []
                song_count += 1
                lyrics = data['artists'][artist]['songs'][song]['lyrics']
                sentences = ''
                for sentence in lyrics.split('\n'):
                    if sentence is not '':
                        sentences = sentences + ' ' + sentence
                        line_count += 1
                tokens = nlp(sentences)
                token_list = []
                rhyme_count = 0
                rhyme_list = []
                word_count = 1
                for token in tokens:
                    if not re.search("\w*[.,\/#!$%\^&\*;:{}=\-_`~()']\w*", token.text):
                        token_list.append(token.text.lower())
                for i in range(0, len(token_list)):
                    current_word = token_list[i]
                    other_words = token_list[i + 1:i + rhyme_cutoff]
                    if current_word not in vocabulary:
                        vocabulary.append(current_word)
                    for j in range(0, len(other_words)):
                        checked_word = other_words[j]
                        if checked_word != None and is_stopword(current_word, STOP_WORDS) == False \
                                and is_stopword(checked_word, STOP_WORDS) == False:
                            word_count += 1
                            if is_rhyme(current_word, checked_word):
                                rhyme_count += 1
                                break
                if artist in rhym_dict:
                    rhym_dict[artist] = rhym_dict.get(artist) + rhyme_count/word_count
                else:
                    rhym_dict[artist] = rhyme_count/word_count
                if artist in vocabulary_size_dict:
                    vocabulary_size_dict[artist] = vocabulary_size_dict.get(artist) + len(vocabulary)
                else:
                    vocabulary_size_dict[artist] = len(vocabulary)
            song_count_dict[artist] = song_count
        else:
            print('skipped: too little songs')
    file.close()
    return song_count_dict, rhym_dict, vocabulary_size_dict

