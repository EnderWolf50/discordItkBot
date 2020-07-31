import discord
from discord.ext import commands
from core.classes import Cog_Ext

import random


class Pins(Cog_Ext):
    @commands.command(aliases=['pin'])
    async def pins(self, ctx):
        msg = await ctx.fetch_message(random.choice(await ctx.channel.pins()).id)
        msgContent = msg.content
        msgAuthor = msg.author.display_name
        await ctx.send(f"{msgAuthor}：{msgContent}")


def setup(bot):
    bot.add_cog(Pins(bot))
