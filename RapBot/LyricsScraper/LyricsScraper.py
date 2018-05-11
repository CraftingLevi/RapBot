"""
Written by Levi van der Heijden
Original Github Repository: -
PURPOSE: Scraping lyrics from the Genius.com API and storing them as txt
DESCRIPTION: LyricsArtist(<String artistname>.scrape_lyrics() stores all lyrics of the specified artist
in a new folder with the artist name as <song_title>.txt. The current script when run does this for
the top 100 rappers of all time (2018)
REQUIRES: An identifier TOKEN (API key) for the Genius API
USEFUL: Acquire a corpus of lyrics to perform NLP operations on for research purposes for advanced analytics
Last Updated: 11-05-2018
"""

from time import sleep
import requests
import simplejson
from bs4 import BeautifulSoup
import re
import os
import time
import datetime
import sys
import logging

# assert the correct python version
assert sys.version_info.major >= 3
"""
This script requires the following constants:
    <TOKEN> in HEADERS = {'Authorization': Bearer <TOKEN>}
    <TOKEN> can be retrieved at https://genius.com/developers
"""

# TODO review store api_token in seperate file to start using public VCS
BASE_URL = "http://api.genius.com"
logger = logging.getLogger(__name__)
file_path = os.getcwd() + "/api_key.txt"
file = open(file_path, 'r', encoding='utf-8')
TOKEN = file.readline()
HEADERS = {'Authorization': "Bearer " + TOKEN}

logging.basicConfig(level=logging.INFO)

"""
The class below scrapes the lyrics of all songs of a given artist
Requires: Artist Name, API-key for authorization
Usage: a = LyricsArtist("<NAME_ARTIST>").store_lyrics()
Output: Creates a folder in this directory with the name of the artist
        Folder includes <song_name>.txt files with lyrics of the <song_name>
logging:
    Depends on logging.BasicConfig(level=<logging_level>)
    DEFAULT = logging.INFO
"""


class LyricsArtist(object):
    def __init__(self, artist):
        logger = logging.getLogger(LyricsArtist.__name__ + ".__init__")
        self.songs_lyrics = {}
        self.artist = artist  # type: str
        self.songs_api_paths = {}
        self.songs = []
        # first, we search for the artist id for the API
        search_url = BASE_URL + "/search"
        params = {'q': artist}
        response = requests.get(search_url, params=params, headers=HEADERS)
        json = response.json()
        artist_id = None
        for hit in json["response"]["hits"]:
            if hit["result"]["primary_artist"]["name"] == self.artist:
                artist_id = hit["result"]["primary_artist"]["id"]
                logger.info("Found the Artist! Starting Scraping...")
                break
        # if we have successfully found the artist, the next code should not terminate the script
        # this code will retrieve the song title and song api id for each song of the artist
        if artist_id is None:
            logger.error('The requested artist (' + artist + ') could not be found')
            sys.exit(1)
        current_page = 1
        next_page = True
        while next_page:
            path = "/artists/{}/songs".format(artist_id)
            params = {'page': current_page}
            response = requests.get(BASE_URL + path, params=params, headers=HEADERS)
            json = response.json()
            page_songs = json['response']['songs']
            if page_songs:
                self.songs += page_songs
                logger.info("I scraped " + str(current_page) + " pages (time: " +
                      datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S') + ')')
                current_page += 1
                sleep(5)
            else:
                next_page = False
                logger.info("Done Scraping!")
        # after all song titles are found and linked with song_api_ids, we write them to
        # self.songs_api_paths where the key is the song name and the value the link to the song info
        for song in self.songs:
            if song["primary_artist"]["id"] == artist_id:
                self.songs_api_paths[song["title"]] = "/songs/" + str(song["id"])

    def scrape_lyrics(self):
        logger = logging.getLogger(LyricsArtist.__name__ + ".scrape_lyrics")
        n = 0
        amount_songs = len(self.songs_api_paths)
        # for each found song, we scrape the lyrics
        for song in self.songs_api_paths:
            song_title = song
            song_url = BASE_URL + self.songs_api_paths.get(song)
            response = requests.get(song_url, headers=HEADERS)
            # BUGFIX: try/catch block for JSONDecodeError
            # CAUSE: most likely a 400 response, skips song in that case
            try:
                json = response.json()
                test_json = True
            except simplejson.scanner.JSONDecodeError:
                test_json = False
                logger.ERROR("Failed to read (" + n + ") " + song_title, exc_info=True)
            if test_json:
                path = json["response"]["song"]["path"]
                # as we have extracted the song url from the api, we can go to the genius webpage
                # from the genious webpage for the song, we extract the HTML
                page_url = "http://genius.com" + path
                page = requests.get(page_url)
                html = BeautifulSoup(page.text, "html.parser")
                # after parsing the HTML, we remove all script elements between the lyrics
                [h.extract() for h in html('script')]
                lyrics = html.find("div", class_="lyrics").get_text()
                lyrics = re.sub("([(\[{]).*?([)\]}])", "", lyrics)
                # we store the songs in a dict with key=title, value=lyrics
                self.songs_lyrics[song_title] = lyrics
                n += 1
                logger.info("I scraped " + str(n) + " of " + str(amount_songs) + " songs (time: " +
                      datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S') + ')')
                sleep(5)
            else:
                n += 1
                sleep(5)
                logger.error("I skipped " + str(n) + "(time: " +
                      datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S') + ')')
        return self.songs_lyrics

    # in this code, we write the lyrics to a file
    # A directory is created for using the artist name if it doesn't already exist
    # A file is created with the name of the song title, and inside the lyrics
    # FIXED BUG: normal codec couldn't write some bytes, thus we use UTF-8 now for encoding
    def store_lyrics(self):
        directory = os.getcwd() + "/Lyrics/" + self.artist
        if not os.path.exists(directory):
            os.makedirs(directory)
        save_path = directory + "/"
        songslist = self.scrape_lyrics()
        for song in songslist:
            file_name = re.sub("[\/\\\]", "-", song)
            file_name = re.sub('[*\.|:?"]', "", file_name)
            lyrics = songslist.get(song)
            file = open(os.path.join(save_path, file_name + ".txt"), "w", encoding='utf-8')
            file.write(lyrics)
            file.close()


def get_lyrics_top100rappers(file_path):
    assert isinstance(file_path, str)
    logger = logging.getLogger(get_lyrics_top100rappers.__name__)
    file = open(file_path, 'r', encoding='utf-8')
    artists = []
    reading = True
    while reading:
        artist = file.readline()
        if artist != '':
            artist = artist.replace('\n', '')
            if "#" not in artist:
                artists.append(artist)
        else:
            reading = False
    failed_artists = []
    for x in range(0, len(artists)):
        logger.info("I am going to scrape " + artists[x])
        try:
            LyricsArtist(artists[x]).store_lyrics()
            logger.info("Succes: " + artists[x])
        except:     #Exceptions are currently unknown
            logger.error("Failed: " + artists[x], exc_info=True)
            failed_artists.append(artists[x])
    logger.debug("Done! I've failed the following artists: ")
    for x in range(0, len(failed_artists)):
        logger.debug(failed_artists[x])
    logger.debug("Check your spelling or look on genius.com how the artist name is stored")


# --------------------------CODE--------------------------#
LyricsArtist("JAY-Z").store_lyrics()

#get_lyrics_top100rappers(os.getcwd() + '/Top100Rappers.txt')



# BIGFIX fix the bug below:
# Traceback (most recent call last):
#   File "C:\Users\Levi\PycharmProjects\practices\Scraper\RapBot\LyricsScraper\LyricsScraper.py", line 118, in <module>
#     LyricsArtist("Childish Gambino").store_lyrics()
#   File "C:\Users\Levi\PycharmProjects\practices\Scraper\RapBot\LyricsScraper\LyricsScraper.py",
#  line 108, in store_lyrics
#     songslist = self.scrape_lyrics()
#   File "C:\Users\Levi\PycharmProjects\practices\Scraper\RapBot\LyricsScraper\LyricsScraper.py",
#  line 80, in scrape_lyrics
#     json = response.json()
#   File "C:\Users\Levi\Anaconda3\lib\site-packages\requests\models.py", line 894, in json
#     return complexjson.loads(self.text, **kwargs)
#   File "C:\Users\Levi\Anaconda3\lib\site-packages\simplejson\__init__.py", line 516, in loads
#     return _default_decoder.decode(s)
#   File "C:\Users\Levi\Anaconda3\lib\site-packages\simplejson\decoder.py", line 370, in decode
#     obj, end = self.raw_decode(s)
#   File "C:\Users\Levi\Anaconda3\lib\site-packages\simplejson\decoder.py", line 400, in raw_decode
#     return self.scan_once(s, idx=_w(s, idx).end())
# simplejson.scanner.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
