import discord
from discord.ext import commands


async def reply_then_delete(
    ctx: commands.Context, msg: str, delay: float = 10, **kwargs
) -> discord.Message:
    # 發送訊息
    reply_msg = await ctx.reply(msg, **kwargs, delete_after=delay)
    # 刪除訊息
    if ctx.guild:
        await ctx.message.delete(delay=delay)
    return reply_msg
