"""
auth spencer-maaaaan
desc bot that collects statistics based on emoji usage in participating server
"""
import json, re, logging
import discord
import emojis

logging.basicConfig(level=logging.INFO)

class Client(discord.Client):
    def __init__(self):
        discord.Client.__init__(self)
        
        #loading json containing stats
        with open("stats.json", "r", encoding = "utf-8") as f:
            self.stats = json.load(f)


    async def on_ready(self):
        logging.info("Logged in as {0}".format(self.user))


    async def on_message(self, message):
        #ignoring private messages
        if message.guild == None:
            logging.info("Ignoring DM from {0}".format(message.author))
            return
        
        #defining some variables for later use
        emojilist = list()
        guildID = str(message.guild.id)
        partial_matches = 0

        #checking for custom/partial emoji in message
        custom_matches = re.findall(r"<(a?):([0-9a-zA-Z]*):([0-9]{18})>", message.content)
        
        if custom_matches:
            emojilist.extend(custom_matches)
                
        for emoji in emojis.iter(message.content):
                partial_matches += 1
                emojilist.append(emoji)

        if custom_matches or partial_matches:
            logging.info("Message proccessed in guild {0}, {1} partials and {2} customs".format(str(message.guild), partial_matches, len(custom_matches)))
        
        #going through each emoji in the message and updating counters
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