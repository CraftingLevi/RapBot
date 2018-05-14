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
import wikipedia
import os
import re

import requests
from nltk import tokenize as tok


BASE_URL = "http://api.genius.com"
file_path = os.getcwd() + "/../api_key_genius"
file = open(file_path, 'r', encoding='utf-8')
TOKEN = file.readline()
HEADERS = {'Authorization': "Bearer " + TOKEN}
file_path = os.getcwd() + "/../api_key_spotify"
file = open(file_path, 'r', encoding='utf-8')
SPOTIFY_URL = "https://api.spotify.com/v1/search"
TOKEN_SPOTIFY = file.readline()

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

#TODO integrate this with lyrics scraping
# The function below gathers the following features
# Song Title
# Artist
# Album
# ?Music
# Language
# Genre
# release year
# featuring artists
# duration (in ms)
# danceability
def get_song_metadata():
    file_path = os.getcwd() + "/../Lyrics"
    artists = [f.name for f in os.scandir(file_path) if f.is_dir()]
    for artist in artists:
        songs = [f.name for f in os.scandir(file_path + "/" + artist)]
        for song in songs:
            song = song.replace('.txt', '')
            search_url = BASE_URL + "/search"
            params = {'q': song}
            response = requests.get(search_url, params=params, headers=HEADERS)
            json = response.json()
            print(artist + " " + song)
            song_api_path = None
            for hit in json["response"]["hits"]:
                something_found = False #check if a hit was found
                if hit["result"]["primary_artist"]["name"] == artist and \
                        re.sub('[*\.|:?"]', '', re.sub("[\/\\\]", "-", hit["result"]["title"])) == song:
                    something_found = True
                    song_api_path = hit["result"]["api_path"]
                    print("the song was found!")
                    song_url = BASE_URL + song_api_path
                    response = requests.get(song_url, headers=HEADERS)
                    json = response.json()
                    path = json["response"]["song"]["path"]
                    # scrape the retrieved html
                    page_url = "http://genius.com" + path
                    page = requests.get(page_url)

                    for line in page.text.splitlines():
                        if re.search("var TRACKING_DATA =", line):
                            metadata = ast.literal_eval(((line.partition('=')[2].strip())[:-1])
                                                        .replace('false', 'False').replace('true', 'True')
                                                        .replace('null', 'None'))
                            print(metadata)
                            title = (metadata["Title"])
                            primary_artist = metadata["Primary Artist"]
                            album = metadata["Primary Album"]
                            music_bool = metadata["Music?"]
                            language = metadata["Lyrics Language"]
                            genre = metadata["Tag"]
                            print(title)
                            print(primary_artist)
                            print(album)
                            print(music_bool)
                            print(language)
                            print(genre)
                        if re.search("release_date_components", line):
                            print(line)
                            duration = None
                            featuring_artists = line.split('&quot;authors&quot;:')[1].replace('&quot;', '')\
                                .replace(artist+',', '').split(',sections')[0].split(',')
                            if 'sections:' in featuring_artists[0]:
                                featuring_artists = None
                            year = line.split('release_date_components')[1].replace('&quot;', '').replace(":{year:", '')[:4]
                            if year == ':nul':
                                year = None
                            print(year)
                            print(featuring_artists)
                            #TODO extract more metadata in this way
                    params_spotify = {'offset': 0, 'limit': 1, 'market': 'US', 'type': 'track', 'q': song,
                                      }
                    SPOTIFY_HEADERS = {'Authorization': 'Bearer ' + TOKEN_SPOTIFY}
                    response_spotify = requests.get(SPOTIFY_URL, params=params_spotify, headers=SPOTIFY_HEADERS)
                    json_spotify = response_spotify.json()
                    if json_spotify["tracks"]["items"]:
                        duration = json_spotify["tracks"]['items'][0]["duration_ms"]
                        id_song = json_spotify["tracks"]['items'][0]["id"]
                        AUDIO_FEATURES_URL = 'https://api.spotify.com/v1/audio-features/'
                        response_spotify2 = requests.get(AUDIO_FEATURES_URL + id_song, headers=SPOTIFY_HEADERS)
                        json_spotify2 = response_spotify2.json()
                        danceability = json_spotify2["danceability"]
                    else:
                        duration = None
                        danceability = None
                    print(duration)
                    print(danceability)
                    if re.sub('[*\.|:?"]', '', re.sub("[\/\\\]", "-", title)) == song:
                        print('--NEXT SONG--')
                        break
            if not something_found:
                print("This song does not exist!")





# ---------------CODE--------------------
get_song_metadata()
#clean_up_data('OutKast', False)

# readFile('50 Cent')
