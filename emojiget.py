"""
returns a list of all the emoji in a string
valid emoji can either be "partial" emojis such as unicode emoji, or custom discord emoji
"""
import re
import emojis

def emojiget(string):
    #initializing list and count for partials
    emojilist = list()
    partial_matches = 0

    #checking for custom discord emojis
    custom_matches = re.findall(r"<(a?):([0-9a-zA-Z]*):([0-9]{18})>", string)    
    if custom_matches: 
        custom_matches = [i[1] for i in custom_matches]
        emojilist.extend(custom_matches)
            
    #checking for partial emojis
    for emoji in emojis.iter(string):
        partial_matches += 1
        emoji = emojis.decode(emoji).replace(":", "")
        emojilist.append(emoji)

    return emojilist