import discord
from discord.ext import commands
from core.classes import Cog_Ext

class Basic(Cog_Ext):
    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Ping is {round(self.bot.latency*1000)} ms and... Pong!')

def setup(bot):
    bot.add_cog(Basic(bot))