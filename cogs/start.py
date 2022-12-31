import discord
from discord.ext import commands
from main import Aniwar
import random


class StartCog(commands.Cog):
    def __init__(self, bot: Aniwar):
        self.bot = bot

    @commands.command()
    async def start(self, ctx: commands.Context):
        users = self.bot.db.playerdb
        allcards = self.bot.db.allcards

        user = users.find_one({"_id": ctx.author.id})
        if user is None:
            newCard = {'_id': allcards.count_documents({'hell': None}) + 1,
                       'char': random.randint(1, 17),
                       'rarity': 3,
                       'level': 20,
                       'evo':1,
                       'owner': ctx.author.id
                       }
            allcards.insert_one(newCard)

            newUserData = {'_id': ctx.author.id,
                    'balance': 1000,
                    'selected': newCard['_id'],
                    'level': 0,
                    'dungeon': 1,
                    'subdungeon': 1,
                    'nick': None,
                    'guild': None,
                    't1': None,
                    't2': None,
                    't3': None
                    }
            users.insert_one(newUserData)

            await ctx.send(
                embed=discord.Embed(
                    title=f"{ctx.author.name} Welcome to AniWar",
                    description=f"""A random Character has joined your party. \nPlease check your inventory `.inv`""",
                    color=discord.Color.blue(),
                ).set_footer(
                    text=ctx.author.name,
                    icon_url=ctx.author.avatar_url
                )
            )
        else:
            await ctx.send("**You have already started this bot!**")


def setup(bot: Aniwar):
    bot.add_cog(StartCog(bot))