"""
takes json and generates a graph of the top n items
"""

import json
import matplotlib.pyplot as plt
import numpy as np

#pulling json into dictionary
with open("stats.json", "r") as f:
    stats = json.load(f)

def top(title, guild, n):
    #sorting and trimming dict to be top n items
    guild = sorted(guild.items(), key=lambda x: x[1])[:-n:-1]
    
    #defining axes
    x = [x[0] for x in guild]
    y = [x[1] for x in guild]
    x_pos = np.arange(len(x))

    #init graph with colors
    plt.bar(x_pos, y, zorder=3, color="#6F85D2")
    plt.title(title)
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

    
    #saving figure
    plt.savefig("./fig/"+title+".png")

#driver code for now
#eventually this will be imported into the bot and used to generate images at the will of a command
top("yoshi", stats["417154708713635852"], 10)