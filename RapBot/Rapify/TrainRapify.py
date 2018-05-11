import os, re
from nltk import tokenize as tok

#TODO implement http://anthology.aclweb.org/C/C14/C14-1059.pdf

def deleteNonSongs(artist, delete):
    dir = os.getcwd() + '/../Lyrics/' + artist
    pattern = 'Tracklist|AMA|Album Art|.+Thank You'
    for file in os.listdir(dir):
        if re.search(pattern, file):
            if delete:
                os.remove(os.path.join(dir, file))
                print("deleted " + file)
            else:
                print(file)

def generateWordModel():
    'do nothing'
    #TODO finish method stub

def readFile(artist):
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



#---------------CODE--------------------
#deleteNonSongs('50 Cent', True)
readFile('50 Cent')
