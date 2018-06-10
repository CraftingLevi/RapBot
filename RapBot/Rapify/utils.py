import json
import os
from matplotlib import pyplot as plt
from RapBot.Rapify.RhymeAnalyser import check_the_rhyme_avg, check_the_rhyme, check_the_rhyme_yearly


def plot_rhym_voc_artist_avg(rhym_cutoff=15, refresh=False):
    if refresh:
        count, rhym, voc = check_the_rhyme_avg(rhyme_cutoff=rhym_cutoff)
        file = open(os.path.join(os.getcwd(), 'count'), "w", encoding='utf-8')
        json.dump(count, file, sort_keys=True, indent=4)
        file.close()
        file = open(os.path.join(os.getcwd(), 'rhyme'), "w", encoding='utf-8')
        json.dump(rhym, file, sort_keys=True, indent=4)
        file.close()
        file = open(os.path.join(os.getcwd(), 'voc'), "w", encoding='utf-8')
        json.dump(voc, file, sort_keys=True, indent=4)
        file.close()
    else:
        file = open(os.path.join(os.getcwd(), 'count'), "r", encoding='utf-8')
        data = json.load(file)
        count = data
        file.close()
        file = open(os.path.join(os.getcwd(), 'voc'), "r", encoding='utf-8')
        data = json.load(file)
        voc = data
        file.close()
        file = open(os.path.join(os.getcwd(), 'rhyme'), "r", encoding='utf-8')
        data = json.load(file)
        rhym = data
        file.close()
    x = []
    y = []
    z = []
    names = []
    for artist in voc.keys():
        names.append(artist)
        x.append(voc.get(artist) / count.get(artist))
        y.append(rhym.get(artist) / count.get(artist))
        z.append(count.get(artist))
    x_names = []
    for i in range(0, len(names)):
        x_names.append(i)
    # SCATTER PLOT
    plt.scatter(x, y, s=30)
    plt.xlabel('Average Vocabulary Size per artist')
    plt.ylabel('Average Occurences of Rhyme per artist')
    plt.title('Vocabulary-Rhyme plot by artist')
    for i, txt in enumerate(names):
        plt.annotate(txt, (x[i], y[i]), fontsize=1, xytext=(-10, 3),
                     textcoords='offset points', ha='center', va='bottom',
                     bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.2))
    plotname = "voc-rhyme analysis (per artist)with rhyme_cutoff " + str(rhym_cutoff)
    plt.savefig(os.getcwd() + "/../Plots/" + str(plotname), dpi=1000)
    plt.clf()
    # BAR PLOT VOCABULARY SIZE
    plt.bar(x_names, x)
    plt.xticks(x_names, names, rotation='vertical', fontsize=1)
    plt.xlabel('Artist')
    plt.ylabel('Average vocabulary size per artist')
    plt.title('Average vocabulary size per song per Artist')
    plotname = "voc analysis (per artist) with rhyme_cutoff " + str(rhym_cutoff)
    plt.savefig(os.getcwd() + "/../Plots/" + str(plotname), dpi=1000)
    plt.clf()
    # BAR PLOT RHYME COUNT
    plt.bar(x_names, y)
    plt.xticks(x_names, names, rotation='vertical', fontsize=1)
    plt.xlabel('Artist')
    plt.ylabel('Average rhyme count per song')
    plt.title('Average rhyme count per song per Artist (normalised using wordcount')
    plotname = "Rhyme analysis (per Artist) with rhyme_cutoff " + str(rhym_cutoff)
    plt.savefig(os.getcwd() + "/../Plots/" + str(plotname), dpi=1000)
    plt.clf()
    plt.bar(x_names, z)
    plt.xticks(x_names, names, rotation='vertical', fontsize=1)
    plt.xlabel('Artist')
    plt.ylabel('Sample size')
    plt.title('Sample size per artist')
    plotname = "Sample analysis (per artist) with rhyme_cutoff " + str(rhym_cutoff)
    plt.savefig(os.getcwd() + "/../Plots/" + str(plotname), dpi=1000)
    plt.clf()
    plt.close()


def plot_rhym_voc_artists(cutoff=1000):
    voc, rhym = check_the_rhyme(cutoff=cutoff)
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
    plotname = "cutoff=" + str(cutoff)
    plt.savefig(os.getcwd() + "/../Plots/" + str(plotname))
    plt.clf()
    plt.close()


"""
INPUT: -
OUTPUT: A plot with points representing years over average vocabulary size and average rhyme count
        Output is stored under 'Plots' as 'voc-rhyme analysis (per year).png'
USES: check_the_rhyme_yearly()
"""


def plot_rhym_voc_yearly():
    count, voc, rhym = check_the_rhyme_yearly()
    x = []
    y = []
    z = []
    names = []
    for year in voc.keys():
        print(year)
        if count.get(year) > 10:
            names.append(year)
            x.append(voc.get(year) / count.get(year))
            y.append(rhym.get(year) / count.get(year))
            z.append(count.get(year))
        else:
            print('skipped')
    # SCATTER PLOT
    plt.scatter(x, y, s=30)
    plt.xlabel('Average Vocabulary Size per song')
    plt.ylabel('Average Occurences of Rhyme per song')
    plt.title('Vocabulary-Rhyme plot by year')
    for i, txt in enumerate(names):
        plt.annotate(txt, (x[i], y[i]))
    plotname = "voc-rhyme analysis (per year)"
    plt.savefig(os.getcwd() + "/../Plots/" + str(plotname))
    plt.clf()
    # BAR PLOT VOCABULARY SIZE
    plt.bar(names, x)
    plt.xlabel('Year')
    plt.ylabel('Average vocabulary size per song')
    plt.title('Average vocabulary size per song per year')
    plotname = "voc analysis (per year)"
    plt.savefig(os.getcwd() + "/../Plots/" + str(plotname))
    plt.clf()
    # BAR PLOT RHYME COUNT
    plt.bar(names, y)
    plt.xlabel('Year')
    plt.ylabel('Average rhyme count per song')
    plt.title('Average rhyme count per song per year')
    plotname = "Rhyme analysis (per year)"
    plt.savefig(os.getcwd() + "/../Plots/" + str(plotname))
    plt.clf()
    plt.bar(names, z)
    plt.xlabel('Year')
    plt.ylabel('Sample size')
    plt.title('Sample size per year')
    plotname = "Sample analysis (per year)"
    plt.savefig(os.getcwd() + "/../Plots/" + str(plotname))
    plt.clf()
    plt.close()
