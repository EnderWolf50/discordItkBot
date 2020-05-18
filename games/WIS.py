import discord
from discord.ext import commands
from core.classes import Cog_Ext

WISpy = False

class WIS(Cog_Ext):
    @commands.command()
    async def WIS(self, ctx):
        global WISpy
        if WISpy == False:
            WISpy = True
            await ctx.send(WISpy)
    
    @commands.Cog.listener()
    async def on_message

def setup(bot):
    bot.add_cog(WIS(bot))