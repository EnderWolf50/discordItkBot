import discord
from discord.ext import commands
from core.classes import Cog_Ext

import unicodedata

class Unicode(Cog_Ext):
    @commands.command(aliases= ["Uni"])
    async def Unicode(self, ctx, E_input):
        try:
            Name = unicodedata.name(E_input)
            await ctx.send(f"{E_input} {Name}")
        except TypeError:
            await ctx.send(f"{E_input} is not unicode character.")
        await ctx.message.delete(delay= 3)

def setup(bot):
    bot.add_cog(Unicode(bot))