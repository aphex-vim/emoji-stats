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

    #executed when the bot logs in to discord
    async def on_ready(self):
        logging.info("Logged in as {0}".format(self.user))
        
        #loading up dictionary of counts
        if os.path.exists("stats.json"):
            with open("stats.json", "r") as f:
                self.stats = json.load(f)

        else:
            self.stats = {}
        
        logging.info("Checking for any new channels/guilds...")

        #loading up set of channels that existed on last run
        if os.path.exists("cached_channels.dat"):
            with open("cached_channels.dat", "rb") as f:
                self.cached_channels = pickle.load(f)

            #forming a set of channels that are new since the last time the bot was online
            present_channels = set()
            
            for guild in self.guilds:
                for chan in guild.text_channels:
                    present_channels.add(chan.id)

            new_channels = present_channels.difference(self.cached_channels)

            #iterating through all new channels and scrubbing them from their beginnings
            for chanID in new_channels:
                chan = await self.fetch_channel(chanID)
                await self.scrub_history(chan, None)

            #writing channels to cache
            with open("cached_channels.dat", "wb") as f:
                pickle.dump(present_channels, f)

        #assuming this file doesn't exist, all channels should be scrubbed
        else:
            self.cached_channels = set()
            
            for guild in self.guilds:
                for chan in guild.text_channels:
                    self.cached_channels.add(chan.id)
                    
            #writing channels to cache
            with open("cached_channels.dat", "wb") as f:
                pickle.dump(self.cached_channels, f)
                    
            
            #iterating through every now-cached channel and scanning from their beginnings
            for chanID in self.cached_channels:
                chan = await self.fetch_channel(chanID)
                await self.scrub_history(chan, None)

        logging.info("New channels checked!")
        logging.info("Catching up on missed messages...")


        #determining how far to look back by lookinginto timelastscanned
        if os.path.exists("time_last_scanned.dat"):
            with open("time_last_scanned.dat", "rb") as f:
                lastscanned = pickle.load(f)

        else:
            lastscanned = None

        #looking through every guild since the last 
        for guild in self.guilds:
            for channel in guild.text_channels:
                await self.scrub_history(channel, lastscanned)

        logging.info("Proccessed any missed messages! Awaiting new messages.")
        

    #scrubs the history of a channel from the time supplied to the present
    async def scrub_history(self, chan, last):
        for message in await chan.history(limit=None, after=last).flatten():
            
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
                with open("time_last_scanned.dat", "wb") as f:
                    pickle.dump(datetime.datetime.utcnow(), f)

                #dumping list to json
                with open("stats.json", "w") as f:
                    f.write(json.dumps(self.stats))           


    #what should happen any time the bot recieves a message
    async def on_message(self, message):
        #ignoring private messages
        if message.guild == None:
            logging.info("Ignoring DM from {0}".format(message.author))
            return

        #ignoring messages sent by bots
        if message.author.bot:
            logging.info("Ignoring bot message in {0}, {1}".format(message.guild.name, message.channel.name))
            return

        #if messages is from a new channel, scrubbing it
        if message.channel.id not in self.cached_channels:
            await self.scrub_history(message.channel, None)
            
            #writing new channel to cache
            with open("cached_channels.dat", "wb") as f:
                self.cached_channels.add(message.channel.id)
                pickle.dump(self.cached_channels, f)
            
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
        with open("time_last_scanned.dat", "wb") as f:
            pickle.dump(datetime.datetime.utcnow(), f)
        
        #dumping list to json
        with open("stats.json", "w") as f:
            f.write(json.dumps(self.stats))
        
#init client object and starting the bot with secret token
client = Client()

with open("token", "r") as f:
    TOKEN = f.read()

client.run(TOKEN)