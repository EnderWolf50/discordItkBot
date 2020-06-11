import discord
from discord.ext import commands
from core.classes import Cog_Ext

import unicodedata

class Unicode(Cog_Ext):
    @commands.command(aliases= ["Uni"])
    async def Unicode(self, ctx, arg):
        try:
            Name = unicodedata.name(arg)
            await ctx.send(f"{arg} {Name}")
        except TypeError:
            await ctx.send(f"{arg} is not unicode character.")

def setup(bot):
    bot.add_cog(Unicode(bot))