from bot import ItkBot
from discord.ext import commands

__all__ = [
    "CogInit",
]


class CogInit(commands.Cog):
    def __init__(self, bot: ItkBot) -> None:
        self.bot = bot
