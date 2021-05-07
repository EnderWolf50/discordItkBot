import discord
from discord.ext import commands
from core import CogInit

import random


class Choose(CogInit):
    @commands.command(aliases=['ch'])
    async def choose(self, ctx: commands.Context, *choices) -> None:
        await ctx.author.send(random.choice(choices))
        await ctx.message.delete(delay=3)


def setup(bot) -> None:
    bot.add_cog(Choose(bot))
