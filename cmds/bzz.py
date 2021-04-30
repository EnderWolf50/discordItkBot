import discord
from discord.ext import commands
from core import CogInit, Mongo

import random, datetime
from datetime import datetime as dt

bzz_options = [
    "大凶",
    "小凶",
    "凶",
    "平",
    "吉",
    "小吉",
    "大吉",
    "吉掰",
    "大吉掰",
    '<:i11_chiwawa:783346447319171075>',
]


class Bzz(CogInit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._db = 'discord_669934356172636199'
        self._coll = 'tdbzz_record'

    @commands.command()
    async def bzz(self, ctx):
        await ctx.send(ctx.author.mention + "：" + random.choice(bzz_options),
                       delete_after=15)

    @commands.command()
    async def tdbzz(self, ctx):
        record = {}
        bzz_msg = ''
        now = dt.now()
        record = Mongo.find(self._db, self._coll,
                            {'_id': now.strftime('%Y-%m-%d')})

        if not record or str(ctx.author.id) not in record.keys():
            bzz_msg = random.choice(bzz_options)
            Mongo.update(self._db, self._coll,
                         {'_id': now.strftime('%Y-%m-%d')},
                         {'$set': {
                             f'{ctx.author.id}': bzz_msg,
                         }})
        else:
            bzz_msg = record[f'{ctx.author.id}']

        await ctx.message.delete(delay=3)
        await ctx.send(ctx.author.mention +
                       f" 你今日（{now.strftime('%m / %d')}）的運勢為：" + bzz_msg,
                       delete_after=15)


def setup(bot):
    bot.add_cog(Bzz(bot))
