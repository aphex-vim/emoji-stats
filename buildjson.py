"""
script for building initial database, will look through message history in all available channels and build json
"""
import json, datetime, pickle, os, logging
import discord
import emojis
from emojiget import emojiget

logging.basicConfig(level=logging.INFO)

class Client(discord.Client):
    def __init__(self):
        discord.Client.__init__(self)
        self.stats = {}

    async def on_ready(self):
        logging.info("Logged in as {0}".format(self.user))

        #loading up existing dictionary
        if os.path.exists("stats.json"):
            with open("stats.json", "r") as f:
                self.stats = json.load(f)

        #determining how far to look back
        if os.path.exists("timelastscanned.dat"):
            with open("timelastscanned.dat", "rb") as f:
                lastscanned = pickle.load(f)

        else:
            lastscanned = None

        #going through every channel in every guild the bot is in
        for guild in self.guilds:
            for channel in guild.text_channels:                
                    for message in await channel.history(limit=None, after=lastscanned).flatten():
                        
                        #making sure music bots are ignored
                        if not message.author.bot:
                            
                            #defining some variables for later use
                            guildID = str(message.guild.id)
                            authorID = str(message.author.id)

                            #checking for custom/partial emoji in message
                            emojilist = emojiget(message.content)

                            if emojilist:
                                logging.info("Message proccessed in guild {0}, channel {1}, author {2}: {3} emojis".format(str(message.guild), message.channel.name, str(message.author), len(emojilist)))

                            #going through each emoji in the message and updating dictionary
                            for emoji in emojilist:
                                emoji = str(emoji)
                                if guildID in self.stats:
                                    
                                    if authorID in self.stats[guildID]:
                                        
                                        if emoji in self.stats[guildID][authorID]:
                                            self.stats[guildID][authorID][emoji] += 1

                                        else:
                                            self.stats[guildID][authorID][emoji] = 1

                                    else:
                                        self.stats[guildID][authorID] = {emoji: 1}

                                else:
                                    self.stats[guildID] = {authorID: {emoji: 1}}
                            
                                #storing time message was scanned to eliminate the need to scan a message more than once
                                with open("timelastscanned.dat", "wb") as f:
                                    pickle.dump(datetime.datetime.utcnow(), f)


                            #dumping list to json
                            with open("stats.json", "w") as f:
                                f.write(json.dumps(self.stats))

        await self.logout()
                    

#init client object and starting the bot with secret token
client = Client()

with open("token", "r") as f:
    TOKEN = f.read()

client.run(TOKEN)