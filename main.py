import discord
from discord.ext import commands
import json
import random
import os

bot = commands.Bot(command_prefix= ".")

with open("others.json", 'r', encoding= "utf8") as jothers:
    other = json.load(jothers)

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

@bot.event
async def on_ready():
    print("Bot is ready.")

@bot.event
async def on_message(msg):
    if "窩不知道" in msg.content:
        await msg.channel.send(random.choice(other["IDK_url"]))
    await bot.process_commands(msg)


for Filename in os.listdir("./cmds"):
    if Filename.endswith(".py"):
        bot.load_extension(F"cmds.{Filename[:-3]}")

if __name__ == "__main__":
    bot.run("NzEwNDk4MDg0MTk0NDg0MjM1.Xr1WWQ.H0OcO7XyHrderg6rCVJFfiWEZiA")