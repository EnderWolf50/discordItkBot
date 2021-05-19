import logging

from discord.ext import commands

from bot.configs import Bot

logger = logging.getLogger(__name__)

__all__ = [
    "ItkBot",
]


class ItkBot(commands.Bot):
    def __init__(self, *args, **options) -> None:
        super().__init__(*args, **options)

    def load_all_extensions(self) -> None:
        from bot.core import EXTENSIONS

        extensions = set(EXTENSIONS)
        for ext in extensions:
            self.load_extension(ext)

    def add_cog(self, cog: commands.Cog) -> None:
        super().add_cog(cog)
        logger.info(f"LOADED | {cog.qualified_name}")

    async def on_ready(self) -> None:
        from random import choice

        from bot.configs import Emojis

        logger.info("Bot is ready.")
        await self.get_channel(Bot.log_channel).send(
            f"親愛的海倫向你早安 {choice(Emojis.helens)}"
        )

    async def on_command(self, ctx: commands.Context) -> None:
        logger.trace(f"{ctx.author} ({ctx.author.id}) | `{ctx.message.content}`")
