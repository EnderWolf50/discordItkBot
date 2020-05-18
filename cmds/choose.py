import discord
from discord.ext import commands
from core.classes import Cog_Ext
import random

class Choose(Cog_Ext):
    @commands.command()
    async def choose(self, ctx, *,arg):
        list = arg.split(" ")
        await ctx.author.send(random.choice(list))
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(Choose(bot))