import requests
from bs4 import BeautifulSoup
import re
#id = "l0G8rdFegrKW1kebyS3sPRUsrc5HJpgMoTgy3hGL990two8cIdYQW5yC9S4UZ-d9"
#secret = "ewgrUuJnoJUogWhl8H5mqUYRTGIer-KvQIITdi41UkM1OOzFunsMKvlAvKAGaiuzFleqfRL91ow9rRWKMKW86w"

"""
These variables are essential. 
headers contains API_KEY. This should be written to a private local file before VCS is implemented
"""
base_url = "http://api.genius.com"
headers = {'Authorization': "Bearer wbZDUP8Er_NE_RoXB_HO8V7ZBWDHCxuUav4Z4yi6r0BujUgKeleEoEsDkxuXDnDM"}


"""
The class below is legacy
Based on a song title and the name of the artist, finds the lyrics
"""
class SongLyrics:
    def __init__(self, song_title, artist_name):
        self.song_title = song_title
        self.artist_name = artist_name
        search_url = base_url + "/search"
        params = {'q': song_title}
        response = requests.get(search_url, params=params, headers=headers)
        json = response.json()
        print(json)
        self.song_api_path = None
        for hit in json["response"]["hits"]:
            if hit["result"]["primary_artist"]["name"] == self.artist_name:
                self.song_api_path = hit["result"]["api_path"]
                print("the song was found!")

    def getLyrics(self):
        if(self.song_api_path == None):
            print("Artist or Song not found")
            return
        song_url = base_url + self.song_api_path
        response = requests.get(song_url, headers = headers)
        json = response.json()
        path = json["response"]["song"]["path"]

        #scrape the retrieved html
        page_url = "http://genius.com" + path
        page = requests.get(page_url)
        html = BeautifulSoup(page.text, "html.parser")

        #remove script tags from lyrics
        [h.extract() for h in html('script')]

        lyrics = html.find("div", class_= "lyrics").get_text()
        lyrics = re.sub("([\(\[]).*?([\)\]])", "", lyrics)
        return lyrics


In_Da_Club = SongLyrics('In Da Club', '50 Cent')
print(In_Da_Club.getLyrics())


