


"""
script for building initial database, will look through message history in all available channels and build json
"""
import json, re, logging
import discord
import emojis

logging.basicConfig(level=logging.INFO)

class Client(discord.Client):
    def __init__(self):
        discord.Client.__init__(self)
        self.stats = {}

    async def on_ready(self):
        logging.info("Logged in as {0}".format(self.user))

        #going through every channel in every guild the bot is in
        for guild in self.guilds:
            for channel in guild.text_channels:                
                    for message in await channel.history(limit=10000).flatten():
                        
                        #making music bots are ignored
                        if not message.author.bot:
                            
                            #defining some variables for later use
                            emojilist = list()
                            guildID = str(message.guild.id)
                            authorID = str(message.author.id)
                            partial_matches = 0

                            #checking for custom/partial emoji in message
                            custom_matches = re.findall(r"<(a?):([0-9a-zA-Z]*):([0-9]{18})>", message.content)
                            
                            if custom_matches: 
                                custom_matches = [i[1] for i in custom_matches]
                                emojilist.extend(custom_matches)
                                    
                            for emoji in emojis.iter(message.content):
                                partial_matches += 1
                                emoji = emojis.decode(emoji).replace(":", "")
                                emojilist.append(emoji)

                            if emojilist:
                                logging.info("Message proccessed in guild {0}, channel {1}, author {2}: {3} partials and {4} customs".format(str(message.guild), channel.name, str(message.author), partial_matches, len(custom_matches)))

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
                            
                            #dumping list to json
                            with open("stats.json", "w") as f:
                                f.write(json.dumps(self.stats))

        await self.logout()
                    

#init client object and starting the bot with secret token
client = Client()

with open("token", "r") as f:
    TOKEN = f.read()

client.run(TOKEN)