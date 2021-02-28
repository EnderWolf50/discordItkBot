import discord
from discord.ext import commands
from core.classes import Cog_Ext

import unicodedata
import logging

logger = logging.getLogger(__name__)


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

    @commands.command()
    async def cls(self, ctx):
        if ctx.channel.type != discord.ChannelType.private: return

        msgList = await ctx.channel.history(limit=None).flatten()

        for msg in msgList:
            if msg.author == self.bot.user:
                await msg.delete()

    @commands.command(aliases=["Emoji", "Emo", "Unicode", "Uni"])
    async def Emo_search(self, ctx, *, E_input):
        if E_input.startswith(":") and E_input.endswith(":"):
            E_input = E_input.strip(":")
        try:
            Emoji = await commands.EmojiConverter().convert(ctx, E_input)
        except:
            try:
                Name = unicodedata.name(E_input)
            except:
                await ctx.send("Input Error!")
            else:
                await ctx.send(f"{E_input} {Name}")
        else:
            if Emoji.animated:
                await ctx.send(f"\<a:{Emoji.name}:{Emoji.id}>")
            else:
                await ctx.send(f"\<:{Emoji.name}:{Emoji.id}>")
        await ctx.message.delete(delay=3)


def setup(bot):
    bot.add_cog(Others(bot))
