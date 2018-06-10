from RapBot.LyricsScraper.LyricsScraper import get_lyrics_artists

"""
Created by Levi van der Heijden
This script is used to run the LyricsScraper without having to open the code
REQUIRED: an api key is stored in a txt file named api_key_genius in the folder RapBot, such that
            <ProjectName>/RapBot/api_key_genius.
INPUT: change the variables 'file_name' and 'language' to appropriate values
OUTPUT: Scrapes lyrics of the artists provided in a txt file given in file_name
"""

# The variable of file_name should be a txt file in the same folder as the api_key_genius file
# The list should contain artist names, seperated by an enter.
# EXAMPLE:
# Kanye West
# Drake
# when this script is run, and an artist has been scraped, the list will change to exclude a succfully scraped artist
# in a next run
# EXAMPLE AFTER A RUN WHERE KANYE WEST WAS SCRAPED BUT DRAKE NOT
# #Kanye West
# Drake
file_name = 'Top100Rappers.txt'

# The variable language should be a string with the language code for said language
# EXAMPLE FOR THE ENGLISH LANGUAGE
# 'en'
# EXAMPLE FOR THE DUTCH LANGUAGE
# 'nl'
language = 'en'


get_lyrics_artists(file_name=file_name, language=language)