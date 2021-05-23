from datetime import datetime, timedelta
from enum import Enum
from typing import Optional

import discord
from discord.ext import commands
from pytz import timezone


class MessageUtils:
    @staticmethod
    async def reply_then_delete(
        ctx: commands.Context,
        msg: str,
        msg_1_delay: float = 10,
        msg_2_delay: Optional[float] = None,
        **kwargs
    ) -> discord.Message:
        """回復並在指定秒數後刪除訊息"""
        if msg_2_delay is None:
            msg_2_delay = msg_1_delay
        # 發送訊息
        reply_msg = await ctx.reply(msg, **kwargs, delete_after=msg_1_delay)
        # 刪除訊息
        if ctx.guild:
            await ctx.message.delete(delay=msg_2_delay)
        return reply_msg


class DatetimeUtils(datetime):
    class Weekdays(Enum):
        MONDAY = 0
        TUESDAY = 1
        WEDNESDAY = 2
        THURSDAY = 3
        FRIDAY = 4
        SATURDAY = 5
        SUNDAY = 6

    @staticmethod
    def today_with(
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
        tz: str = "Asia/Taipei",
    ):
        return datetime.now(tz=timezone(tz)).replace(
            hour=hour, minute=minute, second=second, microsecond=microsecond
        )

    @staticmethod
    def tomorrow_with(
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
        tz: str = "Asia/Taipei",
    ):
        return (datetime.now(tz=timezone(tz)) + timedelta(days=1)).replace(
            hour=hour, minute=minute, second=second, microsecond=microsecond
        )

    @staticmethod
    def next_weekday_with(
        wd: Weekdays,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
        microsecond: int = 0,
        tz: str = "Asia/Taipei",
    ):

        _today = datetime.now(tz=timezone(tz))
        _next_weekday = _today + timedelta(days=(wd.value - _today.weekday()) % 7)

        return _next_weekday.replace(
            hour=hour, minute=minute, second=second, microsecond=microsecond
        )
