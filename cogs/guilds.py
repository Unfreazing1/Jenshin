import discord
from discord.ext import commands
from main import Aniwar
import re


class GuildCog(commands.Cog):
    def __init__(self, bot: Aniwar):
        self.bot = bot

    @commands.command()
    async def accept(self, ctx):
        request = self.bot.tempguilddb.find_one({'owner': ctx.author.id,
                                                 'cid': ctx.channel.id})
        if request is None:
            await ctx.send(f"Nothing to accept here")
        else:
            self.bot.playerdb.update_one({'_id': request['request']},
                                         {'$set': {'guild': request['guild']}})
            self.bot.guilddb.update_one({'_id':request['guild']},
                                        {'$inc': {'members': -1}})
            self.bot.tempguilddb.delete_one({'owner': ctx.author.id,
                                           'cid': ctx.channel.id})
            await ctx.send(f"{ctx.author.name} welcomes <@{request['request']}> to their Guild")

    @commands.command()
    async def guild(self, ctx, *, subcommand = None):
        player = self.bot.playerdb.find_one({"_id": ctx.author.id})
        isMember = self.bot.guilddb.find_one({'_id': player['guild']})
        if subcommand is None:
            if playerguild is None:
                embed = discord.Embed(description=f'**{ctx.author.name}** is not in any Guild')
            else:
                pass

        else:
            subcommands = subcommand.strip(' ').split(' ')
            if subcommands[0].lower() == 'create':
                if isMember is not None:
                    embed = discord.Embed(description=f"**{ctx.author.name}** is already a member of **{isMember['guildname']}** guild")
                elif player['balance'] < 100000:
                    embed = discord.Embed(description=f"**{ctx.author.name}** does not have enough gold to establish a guild.")
                else:
                    try:
                        guildid = self.bot.guilddb.count_documents({'hell': None})
                        self.bot.guilddb.insert_one(
                                {
                                    '_id': guildid,
                                    'owner': ctx.author.id,
                                    'members': 1,
                                    'level': 1,
                                    'maxmembers': 10,
                                    'balance': 0,
                                    'guildname': subcommands[1].lower()
                                })
                        self.bot.playerdb.update_one({"_id": ctx.author.id}, {'$set': {'guild': guildid}})
                    except IndexError:
                        embed = discord.Embed(description=f'**{ctx.author.name}** forgot to add guild name. `.guild create [name]`')

            elif subcommands[0].lower() == 'leave':
                if isMember is  None:
                    embed = discord.Embed(description=f"**{ctx.author.name}** is not a member of any guild")
                elif isMember['owner'] == ctx.author.id:
                    embed = discord.Embed(description=f"**{ctx.author.name}** is Guild owner of **{isMember['guildname']}** guild. Transfer ownership before leaving")
                else:
                    embed = discord.Embed(description=f"**{ctx.author.name}** left **{isMember['guildname']}** guild.")
                    self.bot.guilddb.update_one({'_id': isMember['_id']}, {'$inc': {'members': -1}})
                    self.bot.playerdb.update_one({'_id': ctx.author.id}, {'$set': {'guild': None}})

            elif subcommands[0].lower() == 'transfer':
                if isMember is None:
                    embed = discord.Embed(description=f"**{ctx.author.name}** is not a member of any guild")
                elif isMember['owner'] != ctx.author.id:
                    embed = discord.Embed(description=f"**{ctx.author.name}** is not a Owner of any guild")
                else:
                    try:
                        newOwner = int(re.findall(subcommands[1])[0])
                        isNewOwner = self.bot.playerdb.find_one({'_id': newOwner})
                        if isNewOwner['guild'] != isMember['guild']:
                            embed = discord.Embed(description=f"**{newOwner}** is not a Owner of your guild")
                        else:
                            self.bot.guilddb.update_one({'owner': ctx.author.id},
                                                        {'$set': {'owner': newOwner}})
                            embed = discord.Embed(description=f"**{newOwner}** is now Owner of **{isMember['guildname']}** guild")
                    except IndexError:
                        embed = discord.Embed(description=f'**{ctx.author.name}** forgot to add new owner. `.guild transfer [name]`')

            elif subcommands[0].lower() == 'delete':
                if isMember is None:
                    embed = discord.Embed(description=f"**{ctx.author.name}** is not a member of any guild")
                elif isMember['owner'] != ctx.author.id:
                    embed = discord.Embed(description=f"**{ctx.author.name}** is not a Owner of any guild")
                elif isMember['members'] != 1:
                    embed = discord.Embed(description=f"**{ctx.author.name}** can not delete **{isMember['guildname']}** guild as it is not empty")
                else:
                    self.bot.guilddb.delete_one({'owner': ctx.author.id})
                    self.bot.playerdb.update_one({'_id': ctx.author.id},
                                                 {'$set': {'guild': None}})
                    embed = discord.Embed(
                        description=f"**{ctx.author.name}** deleted **{isMember['guildname']}**")

            elif subcommands[0].lower() == 'join':
                if isMember is not None:
                    embed = discord.Embed(description=f"**{ctx.author.name}** is already a member of **{isMember['guildname']}** guild")
                else:
                    try:
                        newOwner = int(re.findall(subcommands[1])[0])
                        isNewOwner = self.bot.guild.find_one({'owner': newOwner})
                        if isNewOwner is None:
                            embed = discord.Embed(description=f"**{newOwner}** is not a Owner of your guild")
                        elif isNewOwner['members'] == isNewOwner['maxmembers']:
                            embed = discord.Embed(description=f"**{isNewOwner['guildname']}** has no free space")
                        else:
                            self.bot.tempguilddb.insert_one({'request': ctx.author.id,
                                                             'owner': isNewOwner['owner'],
                                                             'guild': isNewOwner['_id'],
                                                             'cid': ctx.channel.id})
                            embed = None
                            guildMessage = f"{ctx.author.name} is requesting to join **{isNewOwner['guildname']}**. Allow by using `.accept`"
                    except IndexError:
                        embed = discord.Embed(
                            description=f'**{ctx.author.name}** forgot to add guild owner. `.guild join [ownertag]`')

            elif subcommands[0].lower() == 'kick':
                if isMember is None:
                    embed = discord.Embed(description=f"**{ctx.author.name}** is not a member of any guild")
                elif isMember['owner'] != ctx.author.id:
                    embed = discord.Embed(description=f"**{ctx.author.name}** is not a Owner of any guild")
                else:
                    try:
                        newkick = int(re.findall(subcommands[1])[0])
                        isNewKick = self.bot.playerdb.find_one({'_id': newKick})
                        if newkick == ctx.author.id:
                            embed = discord.Embed(description=f"**{ctx.author.name}**, You can't kick yourself")
                        elif isNewKick['guild'] != isMember['guild']:
                            embed = discord.Embed(description=f"**{newKick}** is not a member of your guild")
                        else:
                            self.bot.guilddb.update_one({'owner': ctx.author.id},
                                                        {'$inc': {'members': -1}})
                            self.bot.playerdb.update_one({'_id': newkick},
                                                         {'$set': {'guild': None}})
                            embed = discord.Embed(
                                description=f"**{newkick}** has been kicked from **{isMember['guildname']}** guild")
                    except IndexError:
                        embed = discord.Embed(
                            description=f'**{ctx.author.name}** forgot to add new owner. `.guild transfer [name]`')

        if embed is None:
            await ctx.send(guildMessage)
        else:
            await ctx.send(embed=embed)


def setup(bot: Aniwar):
    bot.add_cog(GuildCog(bot))