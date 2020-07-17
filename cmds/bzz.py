import discord
from discord.ext import commands
from core.classes import Cog_Ext
from core.rwFile import rFile, wFile

import random
import datetime

class Bzz(Cog_Ext):
    @commands.command()
    async def bzz(self, ctx):
        await ctx.send(ctx.author.mention + "：" + random.choice(["大凶", "小凶", "凶", "平", "吉", "小吉", "大吉", "吉掰", "大吉掰"]))

    @commands.command()
    async def tdbzz(self, ctx):
        record = rFile("record")

        result = rFile("result")

        if f"{ctx.author.id}" in record:
            if record[f"{ctx.author.id}"] != (datetime.datetime.now() + datetime.timedelta(hours= 8)).strftime("%Y.%m.%d"):

                record[f"{ctx.author.id}"] = (datetime.datetime.now() + datetime.timedelta(hours= 8)).strftime("%Y.%m.%d")

                wFile(record, "record")

                bzz_msg = random.choice(["大凶", "小凶", "凶", "平", "吉", "小吉", "大吉", "吉掰", "大吉掰"])

                result[f"{ctx.author.id}"] = bzz_msg

                wFile(result, "result")

            else:
                bzz_msg = result[f"{ctx.author.id}"]

        else:
            record[f"{ctx.author.id}"] = (datetime.datetime.now() + datetime.timedelta(hours= 8)).strftime("%Y.%m.%d")

            wFile(record, "record")

            bzz_msg = random.choice(["大凶", "小凶", "凶", "平", "吉", "小吉", "大吉", "吉掰", "大吉掰"])

            result[f"{ctx.author.id}"] = bzz_msg

            wFile(result, "result")

        Date = (datetime.datetime.now() + datetime.timedelta(hours= 8)).strftime("%m / %d")

        await ctx.message.delete(delay= 3)
        await ctx.send(ctx.author.mention + f" 你今日（{Date}）的運勢為：" + bzz_msg, delete_after= 7)

def setup(bot):
    bot.add_cog(Bzz(bot))