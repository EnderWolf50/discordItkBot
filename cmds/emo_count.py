import discord
from discord.ext import commands
from core.classes import Cog_Ext

import re
from operator import itemgetter


class Emo_count(Cog_Ext):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = self.mongo_client['discord_669934356172636199']
        self.collection = self.db['emoji_counter']

    @commands.Cog.listener()
    async def on_ready(self):
        self.mongo_emojis = [
            db_emo['_id'] for db_emo in self.collection.find()
        ]
        self.guild_emojis = [
            g_emo.id for g_emo in (
                await self.bot.fetch_guild(669934356172636199)).emojis
        ]

        for db_emo in self.mongo_emojis:
            if db_emo not in self.guild_emojis:
                self.collection.delete_one({'_id': db_emo})
        for g_emo in self.guild_emojis:
            if g_emo not in self.mongo_emojis:
                emo = self.bot.get_emoji(g_emo)
                self.collection.insert_one({
                    '_id': g_emo,
                    'name': emo.name,
                    'animated': emo.animated,
                    'count': 0,
                })

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.channel.type not in {
                discord.ChannelType.text, discord.ChannelType.group
        } or msg.guild.id != 669934356172636199 or msg.author.bot:
            return
        msg_emojis = list(set(re.findall(r'<a?:.*?:(\d*)>', msg.content)))
        for m_emo in msg_emojis:
            self.collection.update_one({'_id': int(m_emo)},
                                       {'$inc': {
                                           'count': 1
                                       }})

    @commands.command(aliases=['ecc'])
    async def emo_counter_clear(self, ctx):
        await ctx.message.delete()
        if not (await self.bot.is_owner(ctx.author)): return

        for db_emo in self.mongo_emojis:
            self.collection.delete_one({'_id': db_emo})

    @commands.command(aliases=['ecr', 'err'])
    async def emo_counter_reset(self, ctx):
        await ctx.message.delete()
        if not (await self.bot.is_owner(ctx.author)): return

        self.guild_emojis = [
            g_emo.id for g_emo in (
                await self.bot.fetch_guild(669934356172636199)).emojis
        ]
        for db_emo in self.mongo_emojis:
            if db_emo not in self.guild_emojis:
                self.collection.delete_one({'_id': db_emo})
                continue
            self.collection.update_one({
                '_id': db_emo,
            }, {
                '$set': {
                    'name': self.bot.get_emoji(db_emo).name,
                    'count': 0,
                }
            })
        for g_emo in self.guild_emojis:
            if g_emo not in self.mongo_emojis:
                emo = self.bot.get_emoji(g_emo)
                self.collection.insert_one({
                    '_id': g_emo,
                    'name': emo.name,
                    'animated': emo.animated,
                    'count': 0,
                })
        self.mongo_emojis = [
            db_emo['_id'] for db_emo in self.collection.find()
        ]

    @commands.command(aliases=['er'])
    async def emo_rank(self, ctx, arg=None):
        await ctx.message.delete(delay=3)
        if not arg: arg = 10
        else:
            emo_id = re.search(r'<a?:.*?:(\d*)>', arg)
            if not emo_id:
                arg = int(arg)
        db_emo_list = [{
            'id': db_emo['_id'],
            'name': db_emo['name'],
            'animated': db_emo['animated'],
            'count': db_emo['count'],
        } for db_emo in self.collection.find()]

        emo_rank = sorted(db_emo_list, key=itemgetter('count'), reverse=True)

        if isinstance(arg, int):
            if arg < 10:
                arg = 10
            elif arg > len(emo_rank):
                arg = len(emo_rank)

            embed = discord.Embed(title=f'排名 {arg - 9} ~ {arg}',
                                  description='')
            for i, emo in enumerate(emo_rank[arg - 10:arg], start=1):
                embed.description += f"<{'a' if emo['animated'] else ''}:{emo['name']}:{emo['id']}>`{emo['count']:^3d}`次　"
                if i % 5 == 0:
                    embed.description += '\n\n'
            await ctx.send(embed=embed, delete_after=60)
        elif isinstance(emo_id[1], str):
            index = next((i for (i, e) in enumerate(emo_rank)
                          if e['id'] == int(emo_id[1])), None)
            if index:
                embed = discord.Embed(description=f'''
                    使用次數：{emo_rank[index]["count"]}


                    排名：{index + 1}''')
                embed.set_thumbnail(url=self.bot.get_emoji(int(emo_id[1])).url)
                await ctx.send(embed=embed, delete_after=60)


def setup(bot):
    bot.add_cog(Emo_count(bot))