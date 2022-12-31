import discord
from discord.ext import commands
from main import Aniwar
import random


class EventCog(commands.Cog):
    def __init__(self, bot: Aniwar):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        spawnthreshold = random.randint(1, 40)
        if spawnthreshold in [1,12,23,34]:
            isSpawn = self.bot.activespawns.find_one({'_id': message.channel.id})
            check = True
            if isSpawn is not None:
                new_check = random.randint(2, 20)
                if new_check != 5:
                    check = False
            if check:
                sp = random.randint(19, 37)
                rp = random.randint(1, 4052)
                if rp < 3001:
                    rp = 1
                elif rp < 4001:
                    rp = 2
                elif rp < 4050:
                    rp = 3
                else:
                    rp = 4
                if sp == 18:
                    rp = 2
                embed = discord.Embed(title=f'Some has Summoned ginger',
                              colour=0xff0086)
                if sp < 18:
                    img = f'https://raw.githubusercontent.com/f04102005/AniWar/main/image-db/{sp}_{rp}.png'
                else:
                    img = f'https://raw.githubusercontent.com/nagatoUzumaki/jenshin/main/images/{sp}_{rp}.jpg'
                embed.set_image(url=img)
                check = self.bot.activespawns.delete_one({'_id': message.channel.id})
                check = self.bot.activespawns.insert_one({'_id': message.channel.id, 'sp': sp, 'rp': rp})
                await message.channel.send(embed=embed)

            await self.bot.process_commands(message)


def setup(bot: Aniwar):
    bot.add_cog(EventCog(bot))