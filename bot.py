"""
auth spencer-maaaaan
desc bot that collects statistics based on emoji usage in participating server
"""
import json, logging, re
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

        if re.match(r"<:(.*):([0-9]{18})>", message.content):
            logging.info(message.content)
        #need to account for two cases:
        #   - unicode emoji (some unicode char)
        #   - custom server emoji (string of format "<:emoji_name:unique_emoji_ID">) use regex?


#init client object and starting the bot with secret token
client = Client()

with open("token", "r") as opened:
    TOKEN = opened.read()

client.run(TOKEN)