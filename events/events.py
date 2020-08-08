import discord
from discord.ext import commands
from core.classes import Cog_Ext
from core.rwFile import rFile, get_setting

from datetime import datetime as dt
import random, re

File = rFile('others')

idk = list(File['IDK_url'].keys())
idk_weights = list(File['IDK_url'].values())

mentionReact = File["Mention_react"]

Owner = get_setting("Owner")

actCute = [
    "<:104:737849572314972181>", "<:103:737846127117991986>",
    "<:102:737843533611794463>", "<:105:738030039563501609>",
    "<:106:738031132490072076>"
]

loadingCatEmos = [
    "<:ldc_01:725343128986320916><:ldc_02:725343129011486761><:ldc_03:725343129183584367><:ldc_04:725343129011748976><:ldc_05:725343128604770348>",
    "<:ldc_06:725343128910954547><:ldc_07:725343128839520259><a:ldc_08:725343129892552764><:ldc_09:725343129011617852><:ldc_10:725343128986583059>",
    "<:ldc_11:725343129087115374><:ldc_12:725343128818548737><:ldc_13:725343128822743041><:ldc_14:725343128994840657><:ldc_15:725343129003360346>"
]


class Events(Cog_Ext):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cmdList = []
        for cmd in self.bot.commands:
            self.cmdList.append(cmd.name)
            for alias in cmd.aliases:
                self.cmdList.append(alias)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready.")

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot: return
        if msg.channel == self.bot.get_channel(675956755112394753): return

        # IDK
        if re.search(r"(窩不知道|我不知道|idk)", msg.content.lower()):
            File = rFile("others")["IDK_url"]

            Picture = str(random.choices(idk,
                                         weights=idk_weights)).strip("[]'")

            if Picture == "https://i.imgur.com/x1qmYCT.gif":
                await msg.channel.send(Picture, delete_after=18.68)
            else:
                await msg.channel.send(Picture, delete_after=5)

        # loading cat
        elif re.search(r"(loading cat|ldc|ldcat|\b痾\b|\b痾...\b)",
                       msg.content.lower()):
            await msg.channel.send(loadingCatEmos[0])
            await msg.channel.send(loadingCatEmos[1])
            await msg.channel.send(loadingCatEmos[2])
        # mention
        elif self.bot.user in msg.mentions and len(msg.mentions) == 1:
            await msg.channel.send(random.choice(mentionReact))
        # reaction
        if "ㄐㄐ" in msg.content:
            await msg.add_reaction("\N{AUBERGINE}")
        if "雞雞" in msg.content:
            await msg.add_reaction("<:emoji_101:713997954201157723>")
        if "尻尻" in msg.content:
            await msg.add_reaction("<a:emoji_103:713998749680009250>")
        # 撒嬌
        if re.search(r"(撒嬌|donut|bakery)", msg.author.display_name.lower()):
            await msg.add_reaction(random.choice(actCute))
        if re.search(r"(撒嬌|donut|bakery)", msg.content.lower()):
            await msg.channel.send(random.choice(actCute))

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        # infinity loading cat
        if re.search(
                rf'({loadingCatEmos[0]}|{loadingCatEmos[1]}|{loadingCatEmos[2]})',
                msg.content.lower()):
            await msg.channel.send(loadingCatEmos[0])
            await msg.channel.send(loadingCatEmos[1])
            await msg.channel.send(loadingCatEmos[2])

        # message backup
        if msg.author.bot: return
        if msg.content[1:].split(' ')[0] in self.cmdList: return

        await self.bot.get_channel(741556551143391323).send(
            f'{msg.author.mention}  `{dt.now().strftime("%Y/%m/%d %H:%M:%S")}`\n{msg.content}'
        )
        for attachment in msg.attachments:
            await self.bot.get_channel(741556551143391323).send(
                attachment.proxy_url)
        await self.bot.get_channel(741556551143391323).send('\u200b')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if str(reaction.emoji) == "\N{THUMBS DOWN SIGN}":
            if user == self.bot.get_user(Owner) or user.bot:
                await reaction.message.add_reaction("\N{THUMBS DOWN SIGN}")
            elif reaction.count >= 2:
                await reaction.message.add_reaction("\N{THUMBS DOWN SIGN}")
        elif "ldcat" in reaction.message.content:
            await reaction.message.remove_reaction(reaction, user)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if str(reaction.emoji) == "\N{THUMBS DOWN SIGN}":
            if user == self.bot.get_user(Owner):
                await reaction.message.remove_reaction("\N{THUMBS DOWN SIGN}",
                                                       self.bot.user)
            elif reaction.count == 1:
                await reaction.message.remove_reaction("\N{THUMBS DOWN SIGN}",
                                                       self.bot.user)


def setup(bot):
    bot.add_cog(Events(bot))
