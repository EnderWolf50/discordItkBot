import discord
from discord.ext import commands
from core import CogInit

import random


class Choose(CogInit):
    @commands.command(aliases=['ch'])
    async def choose(self, ctx, *, arg):
        list = arg.split(" ")
        await ctx.author.send(random.choice(list))
        await ctx.message.delete(delay=3)


def setup(bot):
    bot.add_cog(Choose(bot))