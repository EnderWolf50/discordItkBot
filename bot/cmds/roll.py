from random import randint

from core import CogInit
from discord.ext import commands


class Roll(CogInit):
    @commands.command()
    async def roll(self, ctx, max_num: int, *, roll_msg="{}") -> None:
        if max_num <= 0:
            await ctx.send("ㄐㄐ", delete_after=20)
            await ctx.send("雞雞", delete_after=20)
            await ctx.send("尻尻", delete_after=20)

        # 若有指定字元，將字串格式化後送出
        else:
            if "{}" in roll_msg:
                await ctx.reply(roll_msg.replace("{}", str(randint(1, max_num)), 1))
            elif "%" in roll_msg:
                await ctx.reply(roll_msg.replace("%", str(randint(1, max_num)), 1))
            else:
                await ctx.reply(f"{roll_msg} {randint(1, max_num)}%")
            await ctx.message.delete(delay=20)


def setup(bot) -> None:
    bot.add_cog(Roll(bot))
