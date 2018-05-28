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
    rhym_dict ={}
    vocabulary_size_dict = {}
    how_long_still = 0
    for artist in data['artists']:
        how_long_still +=1
        print('done '+ str(how_long_still) +' out of 80')
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
        elif line_count >=cutoff:
            vocabulary_size_dict[artist] = len(vocabulary)
    true_rhym_dict = {}
    for artist in rhym_dict.keys():
        if artist in vocabulary_size_dict:
            true_rhym_dict[artist] = rhym_dict.get(artist)
    return true_rhym_dict, vocabulary_size_dict

#We do not use rijk rijm, as it is inferiour
def is_rhyme(w1, w2):
    if check_eind_rijm(w1, w2) or check_begin_rijm(w1, w2):
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


def word_equalizer_nl(word):
    #TODO integrate list of exceptions
    word = word.replace('d', 't')
    if word.find('c') != -1 and word.find('c') is not len(word) - 1:
        i = word.index('c')
        if word[i+1] in ['e', 'i']:
            word = word.replace('c', 's')
        else:
            word = word.replace('c', 'k')
    if word.find('qu') != -1:
        i = word.index('qu')
        if word[i+1] is 'e':
            word = word.replace('qu', 'k')
        else:
            word = word.replace('qu', 'kw')
    word = word.replace('ij', '?')
    word = word.replace('ei', '?')
    word = word.replace('z', 's')
    word = word.replace('v', 'f')
    word = word.replace('au', 'ou')
    word = word.replace('th', 't')
    word = word.replace('x', 'ks')
    word = word.replace('y', 'i') # the rule of y as 'ie' or 'i' is vague
    word = word.replace('oe', '!')
    word = word.replace('ee', '#')
    word = word.replace('en', 'e')

    return word

def check_eind_rijm(word1, word2):
    word1 = word_equalizer_nl(word1)
    word2 = word_equalizer_nl(word2)
    if len(word1) <= len(word2):
        n=0
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
    return STOP_WORDS

def is_stopword(w, STOP_WORDS=None):
    if STOP_WORDS is None:
        STOP_WORDS = load_stopwords()
    if w in STOP_WORDS:
        return True
    else:
        return False

def plot_rhym_voc(cutoff=1000):
    voc, rhym = check_the_rhyme(cutoff=cutoff)
    # print('VOCABULARY RANKINGS')
    # n = 0
    # for k, v in sorted(voc.items(), key=operator.itemgetter(1), reverse=True):
    #     n += 1
    #     print(n, k, v)
    # n = 0
    # print('RHYM RANKINGS')
    # for k, v in sorted(rhym.items(), key=operator.itemgetter(1), reverse=True):
    #     n += 1
    #     print(n, k, v)
    x = []
    y = []
    names = []
    for artist in voc.keys():
        print(artist)
        names.append(artist)
        x.append(voc.get(artist))
        y.append(rhym.get(artist))
    plt.scatter(x, y, s=30)
    plt.xlabel('Vocabulary Size')
    plt.ylabel('Occurences of Rhyme')
    plt.title('Vocabulary-Rhym plot with cutoff=' + str(cutoff))
    for i, txt in enumerate(names):
        plt.annotate(txt, (x[i], y[i]))
    plotname = "cutoff=" +str(cutoff)
    plt.savefig(os.getcwd() + "/../Plots/" + str(plotname))
    plt.clf()
    plt.close()


# --- CODE----
plot_rhym_voc(cutoff=1000)
plot_rhym_voc(cutoff=2000)
plot_rhym_voc(cutoff=3000)
plot_rhym_voc(cutoff=3500)

