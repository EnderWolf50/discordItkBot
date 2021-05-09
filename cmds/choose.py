import random

from core import CogInit
from core.config import Emojis
from discord.ext import commands


class Choose(CogInit):
    @commands.command(aliases=["ch"])
    async def choose(self, ctx: commands.Context, *choices) -> None:
        await ctx.message.delete(delay=3)
        if len(choices) < 1:
            await ctx.reply(f"你沒有輸入選項 {Emojis.rainbow_pepe_angry}", delete_after=5)
        await ctx.author.send(random.choice(choices))


def setup(bot) -> None:
    bot.add_cog(Choose(bot))
