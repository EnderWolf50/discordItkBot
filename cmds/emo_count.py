import discord
from discord.ext import commands
from core.classes import Cog_Ext

import os, re, pymongo

client = pymongo.MongoClient(
    f"mongodb+srv://Kerati:{os.getenv('MONGO_PASSWORD')}@kerati.o6ymg.mongodb.net/Kerati?retryWrites=true&w=majority"
)

db = client['discord_669934356172636199']
coll = db['emoji_counter']


class Emo_count(Cog_Ext):
    @commands.command(aliases=['ecc'])
    async def emo_counter_clear(self, ctx):
        await ctx.message.delete()
        for db_emo in self.mongo_emojis:
            coll.delete_one({'_id': db_emo})

    @commands.command(aliases=['ecr'])
    async def emo_counter_reset(self, ctx):
        await ctx.message.delete()
        self.guild_emojis = [
            g_emo.id for g_emo in (
                await self.bot.fetch_guild(669934356172636199)).emojis
        ]
        for db_emo in self.mongo_emojis:
            if db_emo not in self.guild_emojis:
                coll.delete_one({'_id': db_emo})
                continue
            coll.update_one({
                '_id': db_emo,
            }, {
                '$set': {
                    'name': self.bot.get_emoji(db_emo).name,
                    'count': 0,
                }
            })
        for g_emo in self.guild_emojis:
            if g_emo not in self.mongo_emojis:
                coll.insert_one({
                    '_id': g_emo,
                    'name': self.bot.get_emoji(g_emo).name,
                    'count': 0,
                })
        self.mongo_emojis = [db_emo['_id'] for db_emo in coll.find()]

    @commands.Cog.listener()
    async def on_ready(self):
        self.mongo_emojis = [db_emo['_id'] for db_emo in coll.find()]
        self.guild_emojis = [
            g_emo.id for g_emo in (
                await self.bot.fetch_guild(669934356172636199)).emojis
        ]

        for db_emo in self.mongo_emojis:
            if db_emo not in self.guild_emojis:
                coll.delete_one({'_id': db_emo})
        for g_emo in self.guild_emojis:
            if g_emo not in self.mongo_emojis:
                coll.insert_one({
                    '_id': g_emo,
                    'name': self.bot.get_emoji(g_emo).name,
                    'count': 0,
                })

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.channel.type not in {
                discord.ChannelType.text, discord.ChannelType.group
        } or msg.guild.id != 669934356172636199:
            return
        msg_emojis = list(set(re.findall(r'<a?:.*?:(\d*)>', msg.content)))
        for m_emo in msg_emojis:
            coll.update_one({'_id': int(m_emo)}, {'$inc': {'count': 1}})


def setup(bot):
    bot.add_cog(Emo_count(bot))