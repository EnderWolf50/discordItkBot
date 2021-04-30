import discord
from discord.ext import commands
from core import CogInit

import random


class Pins(CogInit):
    @commands.command(aliases=['pin'])
    async def pins(self, ctx, user: discord.Member = None):
        if user == None:
            await ctx.message.delete(delay=3)
            msg = await ctx.fetch_message(
                random.choice(await ctx.channel.pins()).id)
            msgContent = msg.content
            msgAuthor = msg.author.display_name
            if len(msg.attachments) == 0:
                await ctx.send(f"{msgAuthor}：\n{msgContent}")
            else:
                for attachment in msg.attachments:
                    await ctx.send(f"{attachment.url}")
        else:
            await ctx.message.delete(delay=3)
            pinList = []
            for pin in (await ctx.channel.pins()):
                if pin.author.id == user.id:
                    pinList.append(pin)
            msg = await ctx.fetch_message(random.choice(pinList).id)
            msgContent = msg.content
            msgAuthor = msg.author.display_name
            if len(msg.attachments) == 0:
                await ctx.send(f"{msgAuthor}：\n{msgContent}")
            else:
                for attachment in msg.attachments:
                    await ctx.send(f"{attachment.url}")


def setup(bot):
    bot.add_cog(Pins(bot))
