"""
discord bot that collects statistics based on emoji usage in participating servers
"""
import json, datetime, pickle, os, logging
import discord
import emojis
from topn import topn
from emojiget import emojiget

logging.basicConfig(level=logging.INFO)

class Client(discord.Client):
    def __init__(self):
        discord.Client.__init__(self)

    async def on_ready(self):
        logging.info("Logged in as {0}".format(self.user))
        logging.info("Catching up on missed messages...")
        
        #making a counter to see how many messages were missed during downtime
        missed = 0

        #loading up existing dictionary
        if os.path.exists("stats.json"):
            with open("stats.json", "r") as f:
                self.stats = json.load(f)

        #determining how far to look back by lookinginto timelastscanned
        if os.path.exists("timelastscanned.dat"):
            with open("timelastscanned.dat", "rb") as f:
                lastscanned = pickle.load(f)

        else:
            lastscanned = None

        #going through every channel in every guild the bot is in
        for guild in self.guilds:
            for channel in guild.text_channels:                
                    for message in await channel.history(limit=None, after=lastscanned).flatten():

                        #counting missed messages
                        missed += 1
                        
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
                            
                            #storing time message was scanned
                            with open("timelastscanned.dat", "wb") as f:
                                pickle.dump(datetime.datetime.utcnow(), f)

                            #dumping list to json
                            with open("stats.json", "w") as f:
                                f.write(json.dumps(self.stats))

        logging.info("Proccessed {0} missed messages! Awaiting new messages.".format(missed))
        

                            


    async def on_message(self, message):
        #ignoring private messages
        if message.guild == None:
            logging.info("Ignoring DM from {0}".format(message.author))
            return

        #ignoring messages sent by bots
        if message.author.bot:
            logging.info("Ignoring bot message in {0}, {1}".format(message.guild.name, message.channel.name))
            return

        #if the message is a user requesting a graph, generate and send it
        if message.content == "|top":
            await message.channel.send(file=discord.File(topn(str(message.guild), str(message.guild.id), 10)))

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

        #storing time message was scanned
        with open("timelastscanned.dat", "wb") as f:
            pickle.dump(datetime.datetime.utcnow(), f)
        
        #dumping list to json
        with open("stats.json", "w") as f:
            f.write(json.dumps(self.stats))
        
#init client object and starting the bot with secret token
client = Client()

with open("token", "r") as f:
    TOKEN = f.read()

client.run(TOKEN)