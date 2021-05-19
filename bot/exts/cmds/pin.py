import random
from datetime import datetime as dt
from datetime import timedelta

import discord
from bot import ItkBot
from bot.configs import Bot, Emojis
from bot.core import CogInit
from bot.utils import reply_then_delete
from discord.ext import commands


class Pin(CogInit):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def _update_pins(self) -> None:
        self._pins = await self.bot.get_channel(Bot.main_channel).pins()
        self._last_update = dt.utcnow()

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await self._update_pins()

    @commands.command()
    async def pin(self, ctx: commands.Context, user: discord.Member = None) -> None:
        if dt.utcnow() - self._last_update >= timedelta(minutes=5):
            await self._update_pins()

        prepared_pin_list = (
            self._pins if user is None else [m for m in self._pins if m.author == user]
        )
        if len(prepared_pin_list) == 0:
            await reply_then_delete(ctx, f"這個人沒有被釘選的訊息 {Emojis.pepe_nopes}")
            return

        random_pin = random.choice(prepared_pin_list)
        if not random_pin.attachments:
            await ctx.send(f"{random_pin.author.display_name}：\n{random_pin.content}")
        else:
            for attachment in random_pin.attachments:
                await ctx.send(f"{attachment.url}")


def setup(bot: ItkBot) -> None:
    bot.add_cog(Pin(bot))
