import discord
from discord.ext import commands
from core.classes import Cog_Ext

import unicodedata


class Others(Cog_Ext):
    @commands.command()
    async def Mconvert(self, ctx, ID):
        Member = await commands.MemberConverter().convert(ctx, ID)
        await ctx.send(Member)
        await ctx.send(Member.status)

    @commands.command(aliases=["t_m", "tm", "t_msg"])
    async def test_message(self, ctx, times: int):
        for i in range(times):
            await ctx.send(f"test message {i + 1}")


def setup(bot):
    bot.add_cog(Others(bot))