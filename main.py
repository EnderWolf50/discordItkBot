import discord
from discord.ext import commands
import json
import random

bot = commands.Bot(command_prefix= ".")

with open("others.json", 'r', encoding= "utf8") as jothers:
    other = json.load(jothers)

@bot.event
async def on_ready():
    print("Bot is ready.")

@bot.command()
async def ping(ctx):
    await ctx.send(f'Ping is {round(bot.latency*1000)} ms and... Pong!')

@bot.event
async def on_message(msg):
    if "窩不知道" in msg.content:
        await msg.channel.send(random.choice(other["IDK_url"]))
    await bot.porcess_commands(msg)

bot.run("NzEwNDk4MDg0MTk0NDg0MjM1.Xr1WWQ.H0OcO7XyHrderg6rCVJFfiWEZiA")