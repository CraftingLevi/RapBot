# UPDATE: A Jupyter Notebook with a option to open in Google Collab exists for the text generation using a "Kanye West.json" created by the LyricsScraper script

# RapBot
A Bot that can scrape lyrics depending on Artists. Will be used to perform sub-projects such as text-based classification,
Text prediction and Text Generation

# The following has been done
The LyricsScraper is now completely functional. 
To run, please use the run_me.py and follow the instructions
If you want to debug some code or want to be aware of the bugs and work arounds, look in the LyricsScraper.py code
KNOWN BUG: Sometimes an artist does exist in Genius, but the search results won't find hits with the artists name
            The WORKAROUND is to go to docs.genius.com, perform a search query for a popular song with the artist
            derive the artist_id from the results (a json file with the first hits)
            put the artist_id in the if-clause in the first for-loop of the __init__ of the class LyricsArtist
           
# The following is worked on:
Under Rapify, the TrainRapify.py and RhymeAnalyser.py code exists
TrainRapify.py is basically a sandbox scripts in which several text analysis techniques are tested out
RhymeAnalyser.py is a in progress code that currently produces several interesting plots using information
about the scraped artists in the 'collection.json' produced by the LyricsScraper. 
The code for the plots exists in utils.py

The TUI.py code is a beginning of a basic textual interface making the utils.py code even easier to run for
unadvanced programmers.
