from RapBot.Rapify.utils import *


#Run your desired code
running = True
while running:
    print("you can enter the following commands:" + '\n'
                                                    "'artists_avg': plot average rhyme over vocabulary per artist" + ' \n' +
          "'artists: plot total rhyme over vocabulary per artist for first random 1500 lyrics" + '\n' +
          "'yearly': plot avg rhyme per vocabulary per year (excluding years with less than 15 songs" + '\n')
    text = input("Input plot choice: ")
    if text == "artists_avg":
        get_refresh = True
        get_cutoff = True
        while get_cutoff:
            cutoff = eval(input("Input how for can the script look back for rhyme words?: "))
            if type(cutoff) is type(1):
                get_cutoff = False
            else:
                print("(" + str(cutoff) + ") is not of type Integer")
        while get_refresh:
            refresh = input("Do you want to reanalyze your dataset? Enter Y/N: ")
            if refresh.lower() == 'y':
                refresh = True
                get_refresh = False
            elif refresh.lower() == 'n':
                refresh = False
                get_refresh = False
            else:
                print("(" + str(refresh) + ') is not a valid input')
        plot_rhym_voc_artist_avg(rhym_cutoff=cutoff, refresh=refresh)
        running = False
    else:
        print("(" + str(text) + ") is not a valid input" + '\n')