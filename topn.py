"""
takes json and generates a graph of the top n items
returns the location of the saved graph
"""

import json

import matplotlib.pyplot as plt
import numpy as np


def topn(guildName, guildID, n):
    with open("stats.json", "r") as f:
        guild = json.load(f)[guildID]
    
    # summing each user's counts into one dict
    counts = dict()
    for user in guild.keys():
        for emoji in guild[user].keys():
            if emoji in counts.keys():
                counts[emoji] += guild[user][emoji]

            else:
                counts[emoji] = guild[user][emoji]

    # sorting and trimming dict to be top n items
    counts = sorted(counts.items(), key=lambda x: x[1])[:-n-1:-1]
    
    # defining axes
    x = [x[0] for x in counts]
    y = [x[1] for x in counts]
    x_pos = np.arange(len(x))

    # init graph with colors
    params = {
        "ytick.color" : "w",
        "xtick.color" : "w",
        "axes.labelcolor" : "w",
        "axes.edgecolor" : "w"
        }
    
    plt.rcParams.update(params)
    
    ax = plt.axes()
    ax.set_facecolor("#40444B")
    plt.bar(x_pos, y, zorder=3, color="#6F85D2")
    plt.title(guildName, color="w")
    plt.xticks(x_pos, x, rotation=90, ma="right")
    
    # placing value labels on each bar
    for i in range(len(y)):
        plt.annotate(y[i], xy=(x_pos[i], y[i]), ha="center", va="bottom", color="w")

    
    # setting yticks to reasonable amounts
    ymax = max(y)
    plt.yticks(np.arange(0, ymax+(ymax//10), step=ymax//10))
    plt.grid(axis="y", alpha=.5, zorder=0)
    
    # scaling view to include labels
    plt.tight_layout()

    # saving figure and clearing plot
    figName = "./fig/"+guildID+".png"
    plt.savefig(figName, facecolor="#36393F")
    plt.cla()

    # returning figure location
    return figName
