import re
import requests
import discord
from discord import Embed
from discord.ext import commands
import asyncio
import random
import pymongo
import os

#shard1 :-   ac-yilvpcz-shard-00-01.duq2zgt.mongodb.net:27017

#shard2 :-  ac-yilvpcz-shard-00-02.duq2zgt.mongodb.net:27017

#shard3 :-  ac-yilvpcz-shard-00-00.duq2zgt.mongodb.net:27017

intents = discord.Intents.all()
intents.messages = True
intents.dm_messages = True
intents.guild_messages = True

class Aniwar(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='.',
            case_insensitive=True,
            help_command=None,
            strip_after_prefix = True,
            intents=intents
        )

        self.cluster = pymongo.MongoClient(
            'connection string')
        self.db = self.cluster["aniwar"]
        self.playerdb = self.db["playerdb"]
        self.guilddb =  self.db["guilddb"]
        self.tempguilddb =  self.db["tempguilddb"]
        self.base = self.db["base"]
        self.activespawns = self.db["activespawns"]
        self.allcards = self.db["allcards"]

        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                self.load_extension(f"cogs.{filename[:-3]}")

        self.card_rarity = {
            1:'Common',
            2:'Rare',
            3:'Super Rare',
            4:'Ultra Rare',
            'r':2,
            'sr':3,
            'ur': 4,
            'c': 1
        }

    async def on_ready(self):
        print(f"{self.user.name} is ready!")

bot = Aniwar()

bot.run(token)
