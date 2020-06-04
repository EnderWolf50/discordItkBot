import discord
from discord.ext import commands
import json
import os
from keep_alive import keep_alive

bot = commands.Bot(command_prefix= ".", case_insensitive= True)

with open("settings.json", "r", encoding= "utf8") as jsettings:
    setting = json.load(jsettings)

@bot.command()
async def load(ctx, folder, extension):
    if ctx.author == bot.get_user(523755296242270210):
        bot.load_extension(f"{folder}.{extension}")
        await ctx.send(f"**{extension}** has been loaded!", delete_after= 3)

@bot.command()
async def unload(ctx, folder, extension):
    if ctx.author == bot.get_user(523755296242270210):
        bot.unload_extension(f"{folder}.{extension}")
        await ctx.send(f"**{extension}** has been unloaded!", delete_after= 3)

@bot.command()
async def reload(ctx, folder, extension):
    if ctx.author == bot.get_user(523755296242270210):
        bot.reload_extension(f"{folder}.{extension}")
        await ctx.send(f"**{extension}** has been reloaded!", delete_after= 3)
"""
@bot.event
async def on_reaction_add(reaction, user):
    await reaction.message.channel.send(f"{reaction.emoji} {reaction.count} {user.mention}")

@bot.event
async def on_reaction_remove(reaction, user):
    await reaction.message.channel.send(f"{reaction.emoji} {reaction.count} {user.mention}")
"""
for Filename in os.listdir("./cmds"):
    if Filename.endswith(".py"):
        bot.load_extension(F"cmds.{Filename[:-3]}")

for Filename in os.listdir("./events"):
    if Filename.endswith(".py"):
        bot.load_extension(f"events.{Filename[:-3]}")

for Filename in os.listdir("./games"):
    if Filename.endswith(".py"):
        bot.load_extension(f"games.{Filename[:-3]}")

if __name__ == "__main__":
    keep_alive()
    bot.run(setting["TOKEN"])