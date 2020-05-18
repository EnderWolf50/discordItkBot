import discord
from discord.ext import commands
import random
import json
from core.classes import Cog_Ext

with open("others.json", "r", encoding= "utf8") as jothers:
    other = json.load(jothers)

class Events(Cog_Ext):
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready.")

    @commands.Cog.listener()
    async def on_message(self, msg):
        if "窩不知道" in msg.content or "idk" in msg.content.lower():
            Picture = str(random.choices(other["IDK_url"], cum_weights = [35, 44, 99, 100])).strip("[]'")
            await msg.channel.send(Picture)

def setup(bot):
    bot.add_cog(Events(bot))