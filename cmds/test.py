import discord
from discord.ext import commands
from core.classes import Cog_Ext


class Test(Cog_Ext):
    pass


def setup(bot):
    bot.add_cog(Test(bot))
