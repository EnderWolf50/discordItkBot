import os
from discord import Intents
from discord.ext import commands

from core import Bot, logging_setup, sentry_setup

logging_setup()
sentry_setup()

bot = commands.Bot(command_prefix=Bot.prefix,
                   case_insensitive=True,
                   intents=Intents.all(),
                   owner_id=Bot.owner)
# 移除原 help 指令
bot.remove_command("help")


def _load_folder_ext(*folders) -> None:
    for folder in folders:
        for file in os.listdir(f"./{folder}"):
            # 非底線開頭且為 .py 結尾
            if not file.startswith("_") and file.endswith(".py"):
                bot.load_extension(f"{folder}.{file[:-3]}")


_load_folder_ext("cmds", "events", "games", "tasks")

if __name__ == "__main__":
    bot.run(Bot.token)
