import random
from datetime import datetime as dt
from datetime import timedelta

import discord
from core import Bot, CogInit, Emojis
from core.utils import reply_then_delete
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
        random_pin: discord.Message = None
        author: discord.Member = None
        content: str = None

        if user is None:
            await ctx.message.delete(delay=3)
            # 檢查並更新 pin 列表
            if dt.utcnow() - self._last_update >= timedelta(minutes=5):
                await self._update_pins()

            random_pin = random.choice(self._pins)
            author = random_pin.author.display_name
            content = random_pin.content
        else:
            await ctx.message.delete(delay=3)
            # 檢查並更新 pin 列表
            if dt.utcnow() - self._last_update >= timedelta(minutes=5):
                await self._update_pins()

            random_pin = random.choice([m for m in self._pins if m.author == user])
            author = random_pin.author.display_name
            content = random_pin.content

        if not random_pin:

            await reply_then_delete(ctx, f"這個人沒有被釘選的訊息 {Emojis.pepe_nope}")
            return
        if not random_pin.attachments:
            await ctx.send(f"{author}：\n{content}")
        else:
            for attachment in random_pin.attachments:
                await ctx.send(f"{attachment.url}")


def setup(bot) -> None:
    bot.add_cog(Pin(bot))
