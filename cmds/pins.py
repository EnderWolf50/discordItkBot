import discord
from discord.ext import commands
from core.classes import Cog_Ext

import random


class Pins(Cog_Ext):
    @commands.command(aliases=['pin'])
    async def pins(self, ctx):
        await ctx.message.delete(delay=3)
        msg = await ctx.fetch_message(random.choice(await ctx.channel.pins()).id)
        msgContent = msg.content
        msgAuthor = msg.author.display_name
        if len(msg.attachments) == 0:
            await ctx.send(f"{msgAuthor}：{msgContent}")
        else:
            for attachment in msg.attachments:
                await ctx.send(f"{attachment.url}")


def setup(bot):
    bot.add_cog(Pins(bot))
