import discord
from discord.ext import commands
from main import Aniwar
import re


class InfoCog(commands.Cog):
    def __init__(self, bot: Aniwar):
        self.bot = bot

    @commands.command(alias=['bal', 'money'])
    async def balance(self, ctx: commands.Context):
        bal = self.bot.playerdb.find_one({"_id": ctx.author.id})
        if bal is not None:
            await ctx.send(f"""**{str(ctx.author)[:-5]}** has **{bal['balance']:,d}**  Gold""")
        else:
            await ctx.send(f"""**{str(ctx.author)[:-5]}** has't started yet, start your jurney with `.start`""")

    @commands.command(alias=['i'])
    async def info(self, ctx: commands.Context, name=None):
        if name != None:
            rgx = re.compile(f'.*{name}.*', re.IGNORECASE)
            cursor = self.bot.base.find_one({'name': rgx})
        else:
            player = self.bot.playerdb.find_one({
                '_id': ctx.author.id
            })
            card = self.bot.allcards.find_one({
                '_id': player['selected']
            })
            cursor = self.bot.base.find_one({
                'charid': card['char'],
                'rarity': card['rarity']
            })
        embed = discord.Embed(title=f"**{cursor['name'].title()}**",
                              colour=0xff0086)

        embed.add_field(name='Element', value=cursor['element'].title(),inline=True)
        embed.add_field(name='Class', value=cursor['class'].title(), inline=True)
        embed.add_field(name='Ability', value=cursor['ability'].title(), inline=True)
        embed.add_field(name="Stats:",
                        value=f"""\n\nHP:      **{cursor['hp']}**\nATK:     **{cursor['atk']}**\nDEF:     **{cursor['defx']}**\nSPD:     **{cursor['spd']}**\n\nTotal:   **{cursor['total']}**""",
                        inline=False)
        embed.set_image(url=f'https://raw.githubusercontent.com/f04102005/AniWar/main/image-db/{cursor["charid"]}_1.png')
        embed.set_thumbnail(url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx: commands.Context):  # ok
        await ctx.send(f'Pong! {round(self.bot.latency*100)}ms')

    @commands.command()
    async def setnick(self, ctx: commands.Context, *, nickname):
        self.bot.playerdb.update_one({"_id": ctx.author.id}, {'$set': {'nick': nickname.strip(' ')}})
        await ctx.send(f'Updated Nickname to **{nickname}**')

    @commands.command()
    async def profile(self, ctx, *, name='haahh'):
        if name == 'haahh' or name.strip(' ') == '':
            details = self.bot.playerdb.find_one({"_id": ctx.author.id})
        else:
            name = re.findall(r'\d+', name)
            name = int(name[0])
            details = self.bot.playerdb.find_one({"_id": name})
        if details is not None:
            guildname = self.bot.guilddb.find_one({'_id': details['guild']})
            if guildname is None:
                g = 'User not in any Guild'
            else:
                g = guildname['name']

            embed = discord.Embed(title=f"{str(ctx.author)[:-5]}",
                                  description=f"""{ctx.author.name}'s Profile\nNickname: **{details['nick']}**
                                  
    Level: **{details['level']}**
    Guild: **{g}**
    Balance: **{details['balance']}** Gold
    Floor: **{details['dungeon']}-{details['subdungeon']}**""",
                                  colour=0xff0086)
            embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            await ctx.send('Could not find the player')

    @commands.command()
    async def cards(self, ctx, *, filters = None):
        desc = 'All the cards you own are shown below\n\n'
        condition = {'owner': ctx.author.id}
        if filters is not None:
            filter = filters.split('-')
            for temp in filter:
                t = temp.split(' ')
                if t[0].lower() in ('r', 'rarity'):
                    try:
                        rarity = self.bot.card_rarity[t[1].lower()]
                        condition['rarity'] = rarity
                    except Exception:
                        await ctx.channel.send('Please mention correct rarity [c, r, sr, ur]')
                elif t[0].lower() in ('e', 'evo'):
                    try:
                        condition['evo'] = int(t[1])
                    except Exception:
                        await ctx.channel.send('Please mention correct evolution')
        cards = self.bot.allcards.find(condition).limit(20)

        embed = discord.Embed(title=f'{str(ctx.author.name)}',
                      description=desc,
                      colour=0xc0c0c0)
        i = 1
        for c in cards:
            cursor = self.bot.base.find_one({'charid': c['char'], 'rarity': c['rarity']})
            embed.add_field(name=f"**#{i} | {cursor['name'].title()} | Evo[{c['evo']}]**",
                            value=f"{self.bot.card_rarity[c['rarity']]} | Level {c['level']} | ID {c['_id']}",
                            inline=False
                            )
            i = i + 1
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.channel.send(embed=embed)

def setup(bot: Aniwar):
    bot.add_cog(InfoCog(bot))