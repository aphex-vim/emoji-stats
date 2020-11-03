"""
auth spencer-maaaaan
desc bot that collects statistics based on emoji usage in participating server
"""
<<<<<<< HEAD
import json, re, logging
=======
import json, logging, re
>>>>>>> ec7199e6e49aee9593ff7eae181d7a3d3dda771b
import discord

logging.basicConfig(level=logging.INFO)

class Client(discord.Client):
    def __init__(self):
        discord.Client.__init__(self)

    async def on_ready(self):
        logging.info("Logged in as {0}".format(self.user))

    async def on_message(self, message):
        
        #returning on bot's own messages
        if message.author == client.user:
            return

        #ignoring private messages
        if message.guild == None:
            logging.info("Ignoring PM")

        #if a custom emoji is in the string
        if re.match(r"<:(.*):([0-9]{18})>", message.content):
            logging.info(message.content)
        
        #it would be best if I traversed each message word by word
        #then I could produce a subset of the message's words where every element is an emoji
        
        #I still need to account for one case:
        #   - unicode emoji (some unicode char)


#init client object and starting the bot with secret token
client = Client()

with open("token", "r") as opened:
    TOKEN = opened.read()

client.run(TOKEN)