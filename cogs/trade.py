import discord
from discord.ext import commands
from main import Aniwar


class Trade(commands.Cog):
    def __init__(self, bot: Aniwar):
        self.bot = bot



def setup(bot: Aniwar):
    bot.add_cog(Trade(bot))