from discord.ext import commands


class CogInit(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot