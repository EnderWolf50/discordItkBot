import discord
from discord.ext import commands
from core.classes import Cog_Ext

class Point(Cog_Ext):
    @commands.commands()
    async def Point(self, ctx):
        pass

def setup(bot):
    bot.add_cog(Point(bot))