import discord
from discord.ext import commands
from core import CogInit

import random


class Pin(CogInit):
    @commands.command()
    async def pin(self,
                  ctx: commands.Context,
                  user: discord.Member = None) -> None:
        if user == None:
            await ctx.message.delete(delay=3)
            random_pin = await ctx.fetch_message(
                random.choice(await ctx.channel.pins()).id)

            author = random_pin.author.display_name
            content = random_pin.content
            if len(random_pin.attachments) == 0:
                await ctx.send(f"{author}：\n{content}")
            else:
                for attachment in random_pin.attachments:
                    await ctx.send(f"{attachment.url}")
        else:
            await ctx.message.delete(delay=3)
            author_pin_list = [
                m for m in (await ctx.channel.pins()) if m.author.id == user.id
            ]
            random_pin = await ctx.fetch_message(
                random.choice(author_pin_list).id)

            author = random_pin.author.display_name
            content = random_pin.content
            if len(random_pin.attachments) == 0:
                await ctx.send(f"{author}：\n{content}")
            else:
                for attachment in random_pin.attachments:
                    await ctx.send(f"{attachment.url}")


def setup(bot) -> None:
    bot.add_cog(Pin(bot))
