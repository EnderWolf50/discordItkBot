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

        with open("result.json", "r", encoding= "utf-8") as jresult:
            result = json.load(jresult)

        with open("points.json", "r", encoding= "utf-8") as jpoints:
            point = json.load(jpoints)

        if f"{ctx.author.id}" in record:
            if record[f"{ctx.author.id}"] != (datetime.datetime.now() + datetime.timedelta(hours= 8)).strftime("%Y.%m.%d"):

                record[f"{ctx.author.id}"] = (datetime.datetime.now() + datetime.timedelta(hours= 8)).strftime("%Y.%m.%d")

                with open("record.json", "w", encoding= "utf-8") as jrecord:
                    json.dump(record, jrecord, indent= 4)

                bzz_msg = str(random.choice(["大凶", "小凶", "凶", "平", "吉", "小吉", "大吉", "吉掰", "大吉掰"]))

                result[f"{ctx.author.id}"] = bzz_msg
                
                with open("result.json", "w", encoding= "utf-8") as jresult:
                    json.dump(result, jresult, indent= 4)

                if f"{ctx.author.id}" in point:
                    point[f"{ctx.author.id}"] += 5

                    with open("points.json", "w", encoding= "utf-8") as jpoints:
                        json.dump(point, jpoints, indent= 4)
                
                else:
                    point[f"{ctx.author.id}"] = 5

                    with open("points.json", "w", encoding= "utf-8") as jpoints:
                        json.dump(point, jpoints, indent= 4)

            else:
                with open("result.json", "r", encoding= "utf-8") as jresult:
                    bzz_msg = result[f"{ctx.author.id}"]
                
        else:
            record[f"{ctx.author.id}"] = (datetime.datetime.now() + datetime.timedelta(hours= 8)).strftime("%Y.%m.%d")

            with open("record.json", "w", encoding= "utf-8") as jrecord:
                json.dump(record, jrecord, indent= 4)

            bzz_msg = str(random.choice(["大凶", "小凶", "凶", "平", "吉", "小吉", "大吉", "吉掰", "大吉掰"]))

            result[f"{ctx.author.id}"] = bzz_msg
                
            with open("result.json", "w", encoding= "utf-8") as jresult:
                json.dump(result, jresult, indent= 4)
        
        Date = (datetime.datetime.now() + datetime.timedelta(hours= 8)).strftime("%m / %d")

        await ctx.message.delete(delay= 3)
        await ctx.send(ctx.author.mention + f" 你今日（{Date}）的運勢為：" + bzz_msg, delete_after= 7)

def setup(bot):
    bot.add_cog(Bzz(bot))