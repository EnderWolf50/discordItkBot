import discord
from discord.ext import commands
from core.classes import Cog_Ext
from core.rwFile import rFile, wFile

class Point(Cog_Ext):
    @commands.command()
    async def Point(self, ctx):
        
        point = rFile("points")

        await ctx.message.delete(delay= 0.5)
        if f"{ctx.author.id}" not in point:
            point[f"{ctx.author.id}"] = 0
            wFile(point, "points")

            await ctx.send(ctx.author.mention + " 目前的點數為 0")
        
        else:
            await ctx.send(ctx.author.mention + f' 目前的點數為 {point[f"{ctx.author.id}"]}')

def setup(bot):
    bot.add_cog(Point(bot))