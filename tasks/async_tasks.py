import discord
from core import CogInit, Bot, Tasks

import asyncio
from datetime import datetime as dt


class AsyncTasks(CogInit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 好棒三點
        async def _three_oclock() -> None:
            await self.bot.wait_until_ready()

            self.channel = self.bot.get_channel(Bot.main_channel)
            while not self.bot.is_closed():
                if dt.now().strftime("%I %M %S") == "03 00 00":
                    pic = discord.File(Tasks.three_oclock)
                    await self.channel.send("好棒，三點了", file=pic)
                await asyncio.sleep(0.5)

        self._THREE_OCLOCK_TASK = self.bot.loop.create_task(_three_oclock())

        # 只剩三小時
        async def _left_three_hours() -> None:
            await self.bot.wait_until_ready()

            self.channel = self.bot.get_channel(Bot.main_channel)
            while not self.bot.is_closed():
                if dt.now().strftime("%w %H %M %S") == "0 21 00 00":
                    pic = discord.File(Tasks.left_three_hours)
                    await self.channel.send(file=pic)
                await asyncio.sleep(0.5)

        self._LEFT_THREE_HOURS_TASK = self.bot.loop.create_task(
            _left_three_hours())

        # 只剩十秒
        async def _left_ten_seconds() -> None:
            await self.bot.wait_until_ready()

            self.channel = self.bot.get_channel(Bot.main_channel)
            while not self.bot.is_closed():
                if dt.now().strftime("%w %H %M %S") == "0 23 59 50":
                    pic = discord.File(Tasks.left_ten_seconds)
                    await self.channel.send(file=pic)
                await asyncio.sleep(0.5)

        self._LEFT_TEN_SECONDS_TASK = self.bot.loop.create_task(
            _left_ten_seconds())


def setup(bot):
    bot.add_cog(AsyncTasks(bot))
