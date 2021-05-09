import logging
import os
from datetime import datetime

from discord import Intents
from discord.ext import commands

from core import Bot, logging_setup, sentry_setup

logging_setup()
sentry_setup()

logger = logging.getLogger("bot")


bot = commands.Bot(
    command_prefix=Bot.prefix,
    case_insensitive=True,
    intents=Intents.all(),
    owner_id=Bot.owner,
)
# 移除原 help 指令
bot.remove_command("help")


@bot.event
async def on_ready() -> None:
    logger.info("Bot is ready")

    await bot.get_channel(Bot.log_channel).send(
        f'你家機器人睡醒囉 `{datetime.now().strftime("%Y/%m/%d %H:%M:%S")}`'
    )


@bot.event
async def on_command(ctx: commands.Context) -> None:
    logger.trace(f"{ctx.author} ({ctx.author.id}) | `{ctx.message.content}`")


def _load_folder_ext(*folders) -> None:
    for folder in folders:
        for file in os.listdir(f"./{folder}"):
            # 非底線開頭且為 .py 結尾
            if not file.startswith("_") and file.endswith(".py"):
                bot.load_extension(f"{folder}.{file[:-3]}")
                logger.info(f"{folder}.{file[:-3]} has been loaded.")


_load_folder_ext("cmds", "events", "games", "tasks")

if __name__ == "__main__":
    bot.run(Bot.token)
