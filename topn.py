"""
takes json and generates a graph of the top n items
"""

import json
import matplotlib.pyplot as plt
import numpy as np


def topn(guildName, guildID, n):
    #sorting and trimming dict to be top n items
    with open("stats.json", "r") as f:
        guild = json.load(f)[guildID]
    
    guild = sorted(guild.items(), key=lambda x: x[1])[:-n+1:-1]
    
    #defining axes
    x = [x[0] for x in guild]
    y = [x[1] for x in guild]
    x_pos = np.arange(len(x))

    #init graph with colors
    plt.bar(x_pos, y, zorder=3, color="#6F85D2")
    plt.title(guildName)
    plt.xticks(x_pos, x, rotation=90, ma="right")
    
    #placing value labels on each bar
    for i in range(len(y)):
        plt.annotate(y[i], xy=(x_pos[i], y[i]), ha="center", va="bottom")

    
    #setting yticks to reasonable amounts
    ymax = max(y)
    plt.yticks(np.arange(0, ymax+(ymax//10), step=ymax//10))
    plt.grid(axis="y", alpha=.5, zorder=0)
    
    #scaling view to include labels
    plt.tight_layout()

    #saving figure and clearing plot
    figName = "./fig/"+guildName+".png"
    plt.savefig(figName)
    plt.cla()

    #returning figure location
    return figName