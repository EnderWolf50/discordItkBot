import logging

from discord import Intents
from discord_slash import SlashCommand

from bot import ItkBot
from bot.configs import Bot
from bot.log import logging_setup, sentry_setup

logging_setup()
sentry_setup()

logger = logging.getLogger("bot")

itk_bot = ItkBot(
    command_prefix=Bot.prefix,
    case_insensitive=True,
    strip_after_prefix=True,
    intents=Intents.all(),
    owner_id=Bot.owner,
)
# 移除原 help 指令
itk_bot.remove_command("help")
itk_bot.load_all_extensions()

slash = SlashCommand(
    client=itk_bot,
    sync_commands=True,
    delete_from_unused_guilds=True,
    sync_on_cog_reload=True,
    override_type=True,
)


if __name__ == "__main__":
    itk_bot.run(Bot.token)
