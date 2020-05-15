import discord
from discord.ext import commands
import json
import random
import os

bot = commands.Bot(command_prefix= ".")

with open("settings.json", "r", encoding= "utf8") as jsettings:
    setting = json.load(jsettings)

@bot.command()
async def load(ctx, extension):
    bot.load_extension(f"cmds.{extension}")
    await ctx.send(f"**{extension}** has been loaded!")

@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f"cmds.{extension}")
    await ctx.send(f"**{extension}** has been unloaded!")

@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f"cmds.{extension}")
    await ctx.send(f"**{extension}** has been reloaded!")

for Filename in os.listdir("./cmds"):
    if Filename.endswith(".py"):
        bot.load_extension(F"cmds.{Filename[:-3]}")

for Filename in os.listdir("./events"):
    if Filename.endswith(".py"):
        bot.load_extension(f"events.{Filename[:-3]}")

if __name__ == "__main__":
    bot.run(setting["TOKEN"])