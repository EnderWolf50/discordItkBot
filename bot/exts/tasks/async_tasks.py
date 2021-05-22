from datetime import timedelta

import discord
from bot import ItkBot
from bot.configs import Bot, Tasks
from bot.core import CogInit
from bot.utils import get_now, today_replace


class AsyncTasks(CogInit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel = self.bot.get_channel(Bot.main_channel)

        today_0 = today_replace()
        next_sunday = today_0 + timedelta(days=(6 - today_0.weekday()) % 7)

        # 好棒三點
        async def three_oclock() -> None:
            if 3 < get_now().hour < 15:
                await discord.utils.sleep_until(today_replace(hour=15))
            else:
                await discord.utils.sleep_until(today_replace(hour=3))

            pic = discord.File(Tasks.three_oclock)
            await self.channel.send("好棒，三點了", file=pic)

        self._THREE_OCLOCK_TASK = self.bot.loop.create_task(three_oclock())

        # 只剩三小時
        async def left_three_hours() -> None:
            await discord.utils.sleep_until(next_sunday + timedelta(hours=21))

            pic = discord.File(Tasks.left_three_hours)
            await self.channel.send(file=pic)

        self._LEFT_THREE_HOURS_TASK = self.bot.loop.create_task(left_three_hours())

        # 只剩十秒
        async def left_ten_seconds() -> None:
            await discord.utils.sleep_until(
                next_sunday + timedelta(hours=23, minutes=59, seconds=50)
            )

            pic = discord.File(Tasks.left_ten_seconds)
            await self.channel.send(file=pic)

        self._LEFT_TEN_SECONDS_TASK = self.bot.loop.create_task(left_ten_seconds())


def setup(bot: ItkBot) -> None:
    bot.add_cog(AsyncTasks(bot))
