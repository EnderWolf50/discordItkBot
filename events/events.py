import discord
from discord.ext import commands
from core.classes import Cog_Ext
from core.rwFile import rFile, get_setting

import random, re

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
        if msg.author.bot: return
        if msg.channel == self.bot.get_channel(675956755112394753): return
        if "窩不知道" in msg.content or "idk" in msg.content.lower():
            File = rFile("others")["IDK_url"]

            Picture = str(random.choices(list(File.keys()), weights= list(File.values()))).strip("[]'")

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
        elif msg.content == "痾" or msg.content.lower() == "ldcat" or msg.content.lower() == "loading cat" or msg.content.lower() == "ldc":
            await msg.channel.send("<:ldc_01:725343128986320916><:ldc_02:725343129011486761><:ldc_03:725343129183584367><:ldc_04:725343129011748976><:ldc_05:725343128604770348>")
            await msg.channel.send("<:ldc_06:725343128910954547><:ldc_07:725343128839520259><a:ldc_08:725343129892552764><:ldc_09:725343129011617852><:ldc_10:725343128986583059>")
            await msg.channel.send("<:ldc_11:725343129087115374><:ldc_12:725343128818548737><:ldc_13:725343128822743041><:ldc_14:725343128994840657><:ldc_15:725343129003360346>")
        elif self.bot.user in msg.mentions and len(msg.mentions) == 1:
             await msg.channel.send(random.choice(rFile("others")["Mention_react"]))

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        if "<:ldc_01:725343128986320916><:ldc_02:725343129011486761><:ldc_03:725343129183584367><:ldc_04:725343129011748976><:ldc_05:725343128604770348>" in msg.content or "<:ldc_06:725343128910954547><:ldc_07:725343128839520259><a:ldc_08:725343129892552764><:ldc_09:725343129011617852><:ldc_10:725343128986583059>" in msg.content or "<:ldc_11:725343129087115374><:ldc_12:725343128818548737><:ldc_13:725343128822743041><:ldc_14:725343128994840657><:ldc_15:725343129003360346>" in msg.content:
            await msg.channel.send("<:ldc_01:725343128986320916><:ldc_02:725343129011486761><:ldc_03:725343129183584367><:ldc_04:725343129011748976><:ldc_05:725343128604770348>")
            await msg.channel.send("<:ldc_06:725343128910954547><:ldc_07:725343128839520259><a:ldc_08:725343129892552764><:ldc_09:725343129011617852><:ldc_10:725343128986583059>")
            await msg.channel.send("<:ldc_11:725343129087115374><:ldc_12:725343128818548737><:ldc_13:725343128822743041><:ldc_14:725343128994840657><:ldc_15:725343129003360346>")
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if str(reaction.emoji) == "\N{THUMBS DOWN SIGN}":
            if user == self.bot.get_user(Owner) or user.bot == True:
                await reaction.message.add_reaction("\N{THUMBS DOWN SIGN}")
            elif reaction.count >= 2:
                await reaction.message.add_reaction("\N{THUMBS DOWN SIGN}")
        elif "ldcat" in reaction.message.content:
            await reaction.message.remove_reaction(reaction, user)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if str(reaction.emoji) == "\N{THUMBS DOWN SIGN}":
            if user == self.bot.get_user(Owner):
                await reaction.message.remove_reaction("\N{THUMBS DOWN SIGN}", self.bot.user)
            elif reaction.count == 1:
                await reaction.message.remove_reaction("\N{THUMBS DOWN SIGN}", self.bot.user)

def setup(bot):
    bot.add_cog(Events(bot))
