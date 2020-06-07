import discord
from discord.ext import commands
from core.classes import Cog_Ext
import json

class Point(Cog_Ext):
    @commands.command()
    async def Point(self, ctx):
        with open("points.json", "r", encoding= "utf8") as jpoints:
            point = json.load(jpoints)

        await ctx.message.delete(delay= 0.5)
        if f"{ctx.author.id}" not in point:
            point[f"{ctx.author.id}"] = 0
            with open("points.json", "w", encoding= "utf8") as jpoints:
                json.dump(point, jpoints, indent= 4)

            await ctx.send(ctx.author.mention + " 目前的點數為 0")
        
        else:
            await ctx.send(ctx.author.mention + f' 目前的點數為 {point[f"{ctx.author.id}"]}')

def setup(bot):
    bot.add_cog(Point(bot))