import discord
from discord.ext import commands
from core.classes import Cog_Ext
from core.rwFile import rFile, get_setting

import random

url = []
url_weights = []

Owner = get_setting("Owner")

class Events(Cog_Ext):
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready.")

    @commands.Cog.listener()
    async def on_message(self, msg):
        global url
        global url_weights
        if "窩不知道" in msg.content or "idk" in msg.content.lower():
            if msg.author != self.bot.user:

                File = rFile("IDK_url")
                for key, value in File.items():
                    url.append(key)
                    url_weights.append(value)

                Picture = str(random.choices(url, weights= url_weights)).strip("[]'")

                if Picture == "https://i.imgur.com/x1qmYCT.gif":
                    await msg.channel.send(Picture, delete_after= 18.68)
                else:
                    await msg.channel.send(Picture, delete_after= 5)
        elif msg.content == "ㄐㄐ":
            await msg.add_reaction("\N{AUBERGINE}")
        elif msg.content == "雞雞":
            await msg.add_reaction("<:emoji_101:713997954201157723>")
        elif msg.content == "尻尻":
            await msg.add_reaction("<a:emoji_103:713998749680009250>")
        elif "痾" in msg.content or msg.content.lower() == "ldcat" or msg.content.lower() == "loading cat":
            await msg.channel.send("<a:ldcat_001:720660862876123166><a:ldcat_002:720660879888351262><a:ldcat_003:720660898406203400><a:ldcat_004:720660908669665371><a:ldcat_005:720660929678803037>")
            await msg.channel.send("<a:ldcat_006:720660939518771262><a:ldcat_007:720660949723512896><a:ldcat_008:720660960850870292><a:ldcat_009:720660972670418954><a:ldcat_010:720660987174453319>")
            await msg.channel.send("<a:ldcat_011:720660998650069013><a:ldcat_012:720661008477323325><a:ldcat_013:720661018262634597><a:ldcat_014:720661027381051393><a:ldcat_015:720661035836768306>")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass

def setup(bot):
    bot.add_cog(Events(bot))