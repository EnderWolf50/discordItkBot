import discord
from discord.ext import commands


async def reply_then_delete(
    ctx: commands.Context, msg: str, delay_1: float = 10, delay_2: float = 10, **kwargs
) -> discord.Message:
    # 發送訊息
    reply_msg = await ctx.reply(msg, **kwargs, delete_after=delay_1)
    # 刪除訊息
    if ctx.guild:
        await ctx.message.delete(delay=delay_2)
    return reply_msg
