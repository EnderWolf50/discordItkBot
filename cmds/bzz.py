import discord
from discord.ext import commands
from core.classes import Cog_Ext
import random
import json
import datetime

class Bzz(Cog_Ext): 
    @commands.command()
    async def bzz(self, ctx):
        await ctx.send(ctx.author.mention + "：" + str(random.choice(["大凶", "小凶", "凶", "平", "吉", "小吉", "大吉", "吉掰", "大吉掰"])))

    @commands.command()
    async def tdbzz(self, ctx):
        with open("record.json", "r", encoding= "utf-8") as jrecord:
            record = json.load(jrecord)

        if f"{ctx.author.id}" in record:
            if record[f"{ctx.author.id}"] != datetime.datetime.now().strftime("%Y.%m.%d"):
                record[f"{ctx.author.id}"] = datetime.datetime.now().strftime("%Y.%m.%d")

                with open("record.json", "w", encoding= "utf-8") as jrecord:
                    json.dump(record, jrecord, indent= 4)

                await ctx.send(ctx.author.mention + "：" + str(random.choice(["大凶", "小凶", "凶", "平", "吉", "小吉", "大吉", "吉掰", "大吉掰"])))
            else:
                await ctx.send(ctx.author.mention + "：你今日已使用過此指令")
        else:
            record[f"{ctx.author.id}"] = datetime.datetime.now().strftime("%Y.%m.%d")

            with open("record.json", "w", encoding= "utf-8") as jrecord:
                json.dump(record, jrecord, indent= 4)

            await ctx.send(ctx.author.mention + "：" + str(random.choice(["大凶", "小凶", "凶", "平", "吉", "小吉", "大吉", "吉掰", "大吉掰"])))

def setup(bot):
    bot.add_cog(Bzz(bot))