import discord
from discord.ext import commands
from main import Aniwar
import random

class MyCog(commands.Cog):
    def __init__(self, bot: Aniwar):
        self.bot = bot

    @commands.command()
    async def claim(self, ctx: commands.Context):
        check = self.bot.activespawns.find_one({'_id': ctx.channel.id})
        if check is not None:
            check2 = self.bot.playerdb.find_one({'_id': ctx.author.id})
            if check2 is not None:
                ok = self.bot.base.find_one({'charid': check['sp']})
                check3 = self.bot.allcards.insert_one( {
                    'owner': ctx.author.id,
                    '_id': self.bot.allcards.count_documents({'hell': None}) + 1,
                    'char': check['sp'],
                    'rarity': check['rp'],
                    'level': random.randint(1,5),
                    'evo': 1
                })
                if check3 is not None:
                    await ctx.send(f'Claimed {ok["name"]} {self.bot.card_rarity[check["rp"]]}')
                    check = self.bot.activespawns.delete_one({'_id': ctx.channel.id})
        else:
            await ctx.send("You haven't started yet, use `.start` to begin your journey")


def setup(bot: Aniwar):
    bot.add_cog(MyCog(bot))