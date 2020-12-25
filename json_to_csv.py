"""
converts json db to csv
"""

import json

#pulling json into dictionary
with open("stats.json", "r") as f:
    stats = json.load(f)

#iterating through each guild and building a csv for eash
for key in stats.keys(): 
    guild = stats[key]
    
    with open("./csv/"+key+".csv", "w") as f:
        for emoji in guild.keys():
            f.write(emoji+",")
        
        f.write("\n")
        
        for count in guild.values():
            f.write(str(count)+",")