"""
auth spencer-maaaaan
desc bot that collects statistics based on emoji usage in participating server
"""
import json, re, logging
import discord

logging.basicConfig(level=logging.INFO)

class Client(discord.Client):
    def __init__(self):
        discord.Client.__init__(self)
        
        #defining partial (non-custom) emoji list
        with open("emoji.txt", "r", encoding = "utf-8") as f:
            self.partials = [line.replace("\n", "") for line in f.readlines()]

    async def on_ready(self):
        logging.info("Logged in as {0}".format(self.user))
            
    async def on_message(self, message):
        
        #returning on bot's own messages
        if message.author == client.user:
            return

        #ignoring private messages
        if message.guild == None:
            logging.info("Ignoring PM")
            return
        
        #creating sublist for message's emoji
        emojilist = list()

        #checking for custom/parital emoji in message
        custom_matches = re.findall(r"<:([0-9a-zA-Z]*):([0-9]{18})>", message.content)
        
        if custom_matches:
            logging.info("custom match")
            emojilist.extend(custom_matches)
                
        for char in message.content:
            if char in self.partials:
                logging.info("partial match")
                emojilist.append(char)

        #for emoji in emojilist, add to guild's emoji counts in dictionary and dump to json
        

#init client object and starting the bot with secret token
client = Client()

with open("token", "r") as opened:
    TOKEN = opened.read()

client.run(TOKEN)