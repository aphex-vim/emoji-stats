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

        #loading json containing stats
        with open("stats.json", "r", encoding = "utf-8") as f:
            self.stats = json.load(f)


    async def on_ready(self):
        logging.info("Logged in as {0}".format(self.user))
            
    async def on_message(self, message):
        
        #returning on bot's own messages
        if message.author == client.user:
            return

        #ignoring private messages
        if message.guild == None:
            logging.info("Ignoring DM from {0}".format(message.author))
            return
        
        #defining variables for later use
        emojilist = list()
        guildID = str(message.guild.id)
        custom_count = 0
        partial_count = 0

        #checking for custom/parital emoji in message
        custom_matches = re.findall(r"<:([0-9a-zA-Z]*):([0-9]{18})>", message.content)
        
        if custom_matches:
            custom_count += len(custom_matches)
            emojilist.extend(custom_matches)
                
        for char in message.content:
            if char in self.partials:
                partial_count += 1
                emojilist.append(char)

        logging.info("Message proccessed, {0} partials and {1} customs".format(partial_count, custom_count))
        
        for emoji in emojilist:
            emoji = str(emoji)
            if guildID in self.stats:
                
                if emoji in self.stats[guildID]:
                    self.stats[guildID][emoji] += 1

                else:
                    self.stats[guildID][emoji] = 1

            else:
                self.stats[guildID] = {emoji: 1}
        
        with open("stats.json", "w", encoding = "utf-8") as f:
            f.write(json.dumps(self.stats, indent = 4))
        

#init client object and starting the bot with secret token
client = Client()

with open("token", "r") as f:
    TOKEN = f.read()

client.run(TOKEN)