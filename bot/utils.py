from datetime import datetime as dt
from typing import Optional

import discord
import pytz
from discord.ext import commands


async def reply_then_delete(
    ctx: commands.Context,
    msg: str,
    delay_1: float = 10,
    delay_2: Optional[float] = None,
    **kwargs
) -> discord.Message:
    if delay_2 is None:
        delay_2 = delay_1
    # 發送訊息
    reply_msg = await ctx.reply(msg, **kwargs, delete_after=delay_1)
    # 刪除訊息
    if ctx.guild:
        await ctx.message.delete(delay=delay_2)
    return reply_msg


def get_now() -> dt:
    return dt.now(tz=pytz.timezone("Asia/Taipei"))


def today_replace(
    hour: int = 0, minute: int = 0, second: int = 0, microsecond: int = 0
) -> dt:
    return get_now().replace(
        hour=hour, minute=minute, second=second, microsecond=microsecond
    )
