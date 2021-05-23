import discord
from bot import ItkBot
from bot.configs import Bot, Tasks
from bot.core import CogInit
from bot.utils import DatetimeUtils


class AsyncTasks(CogInit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # 好棒三點
        async def three_oclock() -> None:
            await self.bot.wait_until_ready()

            _h = DatetimeUtils.now().hour
            if _h < 3:
                await discord.utils.sleep_until(DatetimeUtils.today_with(hour=3))
            elif 3 < _h < 15:
                await discord.utils.sleep_until(DatetimeUtils.today_with(hour=15))
            else:
                await discord.utils.sleep_until(DatetimeUtils.tomorrow_with(hour=3))

            pic = discord.File(Tasks.three_oclock)
            await self.bot.get_channel(Bot.main_channel).send("好棒，三點了", file=pic)

        self._THREE_OCLOCK_TASK = self.bot.loop.create_task(three_oclock())

        # 只剩三小時
        async def left_three_hours() -> None:
            await self.bot.wait_until_ready()

            await discord.utils.sleep_until(
                DatetimeUtils.next_weekday_with(DatetimeUtils.Weekdays.SUNDAY, hour=21)
            )

            pic = discord.File(Tasks.left_three_hours)
            await self.bot.get_channel(Bot.main_channel).send(file=pic)

        self._LEFT_THREE_HOURS_TASK = self.bot.loop.create_task(left_three_hours())

        # 只剩十秒
        async def left_ten_seconds() -> None:
            await self.bot.wait_until_ready()

            await discord.utils.sleep_until(
                DatetimeUtils.next_weekday_with(
                    DatetimeUtils.Weekdays.SUNDAY.SUNDAY, hour=23, minute=59, second=50
                )
            )

            pic = discord.File(Tasks.left_ten_seconds)
            await self.bot.get_channel(Bot.main_channel).send(file=pic)

        self._LEFT_TEN_SECONDS_TASK = self.bot.loop.create_task(left_ten_seconds())


def setup(bot: ItkBot) -> None:
    bot.add_cog(AsyncTasks(bot))
