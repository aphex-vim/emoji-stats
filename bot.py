"""
auth spencer-maaaaan
desc bot that collects statistics based on emoji usage in participating server
"""
import json
import logging
import discord

class Client(discord.Client):
    def __init__(self):
        discord.Client.__init__(self)

    async def on_ready(self):
        print("logged in as {0}".format(self.user))

    async def on_message(self, message):
        
        #returning on bot's own messages
        if message.author == client.user:
            return

        if message.guild == None:
            print("ignoring PM")


#init client object and starting the bot with secret token
client = Client()

with open("token", "r") as opened:
    TOKEN = opened.read().strip()

client.run(TOKEN)