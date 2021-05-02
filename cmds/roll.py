import discord
from discord.ext import commands
from core import CogInit

from random import randint


class Roll(CogInit):
    @commands.command()
    async def roll(self, ctx, num: int, *, roll_msg="{}") -> None:
        if num <= 0:
            await ctx.send("ㄐㄐ")
            await ctx.send("雞雞")
            await ctx.send("尻尻")

        else:
            if "{}" in roll_msg:
                await ctx.reply(roll_msg.replace("{}", str(randint(1, num)),
                                                 1))
            elif "%" in roll_msg:
                await ctx.reply(roll_msg.replace("%", str(randint(1, num)), 1))
            else:
                await ctx.reply(f"{roll_msg} {randint(1, num)}")


def setup(bot) -> None:
    bot.add_cog(Roll(bot))