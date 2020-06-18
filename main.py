import discord
import os
from discord.ext import commands
from core.rwFile import get_setting

from keep_alive import keep_alive

TOKEN = get_setting("TOKEN")

bot = commands.Bot(command_prefix=".", case_insensitive=True)
bot.remove_command("help")

for Filename in os.listdir("./cmds"):
    if Filename.endswith(".py"):
        bot.load_extension(F"cmds.{Filename[:-3]}")

for Filename in os.listdir("./events"):
    if Filename.endswith(".py"):
        bot.load_extension(f"events.{Filename[:-3]}")

for Filename in os.listdir("./games"):
    if Filename.endswith(".py"):
        bot.load_extension(f"games.{Filename[:-3]}")

for Filename in os.listdir("./tasks"):
    if Filename.endswith(".py"):
        bot.load_extension(f"tasks.{Filename[:-3]}")

if __name__ == "__main__":
    keep_alive()
    bot.run(TOKEN)
