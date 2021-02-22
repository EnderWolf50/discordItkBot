import discord
from discord.ext import commands
from core.classes import Cog_Ext
from core.rwFile import rFile, get_setting

from datetime import datetime as dt
from datetime import timedelta
import os, random, re, asyncio, pymongo, logging

File = rFile('others')

mentionReact = File["Mention_react"]

Owner = get_setting("Owner")

logger = logging.getLogger(__name__)

idk_dict = {
    "./images/idk_orig.jpg": 30,
    "./images/idk_kailiu.jpg": 20,
    "./images/idk_too.jpg": 15,
    "./images/idk_flaming.jpg": 10,
    "./images/idk_whatever.jpg": 10,
    "./images/idk_ero.jpg": 10,
    "./images/idk_gif.gif": 5,
}

yeah_list = [
    "./images/yeah.jpg", "./images/noyeah.jpg", "./images/yeahsanxiao.jpg",
    "./images/yeahstarburst.jpg"
]

actCute = [
    "<:096:802991146933420094>", "<:095:802993480632631316>",
    "<:094:802990261436940318>", "<:089:802989279713427456>",
    "<:088:802992462255620126>", "<:087:802985316373233665>",
    "<:086:802991867246673960>"
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
        self.mongo_emojis = []
        self.guild_emojis = []
        for cmd in self.bot.commands:
            self.cmdList.append(cmd.name)
            for alias in cmd.aliases:
                self.cmdList.append(alias)

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready.")
        await self.bot.get_user(523755296242270210).send(
            f'Bot has been started successfully `{dt.now().strftime("%Y/%m/%d %H:%M:%S")}`'
        )

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.channel.id == 675956755112394753: return
        # reaction
        if "ㄐㄐ" in msg.content:
            await msg.add_reaction("\N{AUBERGINE}")
        if "雞雞" in msg.content:
            await msg.add_reaction("<:emoji_101:713997954201157723>")
        if "尻尻" in msg.content:
            await msg.add_reaction("<a:emoji_103:713998749680009250>")

        if msg.author.bot: return
        # IDK
        if re.search(r"(窩不知道|我不知道|idk)", msg.content.lower()):
            pic = random.choices(list(idk_dict.keys()),
                                 weights=list(idk_dict.values()))[0]
            pic_file = discord.File(pic)

            if pic.endswith(".gif"):
                await msg.channel.send(file=pic_file, delete_after=18.68)
            else:
                await msg.channel.send(file=pic_file, delete_after=7)
        # loading cat
        elif re.search(r"(ldc|ldcat|\b痾\b)", msg.content.lower()):
            await msg.channel.send(loadingCatEmos[0])
            await msg.channel.send(loadingCatEmos[1])
            await msg.channel.send(loadingCatEmos[2])
        # 好耶
        elif "好耶" in msg.content:
            pic_file = discord.File(random.choice(yeah_list))
            await msg.channel.send(file=pic_file, delete_after=5)
        # 交朋友
        elif "交朋友" in msg.content:
            pic_file = discord.File("./images/make_friends.jpg")
            await msg.channel.send(file=pic_file, delete_after=10)
        # 很嗆是吧
        elif re.search(r"很嗆(?:是吧|[喔欸])?|嗆[喔欸]", msg.content.lower()):
            pic_file = discord.File('./images/flaming.jpg')
            await msg.channel.send(file=pic_file, delete_after=7)
        # mention
        elif self.bot.user in msg.mentions:
            await msg.channel.send(random.choice(mentionReact))
        # 撒嬌
        if re.search(r"(撒嬌|donut|bakery)", msg.author.display_name.lower()):
            await msg.add_reaction(random.choice(actCute))
        if re.search(r"(撒嬌|donut|bakery)", msg.content.lower()):
            send_emo = random.randint(0, 4)
            if send_emo != 4:
                await msg.channel.send(random.choice(actCute))
            else:
                await msg.channel.send(f"還敢撒嬌阿 {msg.author.mention}")

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        if msg.channel.type != discord.ChannelType.private and msg.guild.id == 725295821456801842:
            return
        # infinity loading cat
        if re.search(
                rf'({loadingCatEmos[0]}|{loadingCatEmos[1]}|{loadingCatEmos[2]})',
                msg.content.lower()):
            await msg.channel.send(loadingCatEmos[0])
            await msg.channel.send(loadingCatEmos[1])
            await msg.channel.send(loadingCatEmos[2])

        # message backup
        if msg.channel.type == discord.ChannelType.private: return
        if msg.author.bot: return
        if msg.content[1:].lower().split(' ')[0] in self.cmdList: return

        await self.bot.get_channel(741556551143391323).send(
            f'{msg.author.display_name}  `{msg.created_at.strftime("%Y/%m/%d %H:%M:%S")}`\n{msg.content}'
        )
        for attachment in msg.attachments:
            await self.bot.get_channel(741556551143391323).send(
                attachment.proxy_url)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if str(reaction.emoji) == "\N{THUMBS DOWN SIGN}":
            if user == self.bot.get_user(Owner) or user.bot:
                await reaction.message.add_reaction("\N{THUMBS DOWN SIGN}")
            elif reaction.count >= 2:
                await reaction.message.add_reaction("\N{THUMBS DOWN SIGN}")
        if "ldcat" in reaction.message.content:
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

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        logger.info(
            f'{ctx.author.display_name} ({ctx.author.name}#{ctx.author.discriminator}) 執行指令 {ctx.message.content[1:]} 成功'
        )

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        logger.error(
            f'{ctx.author.display_name} ({ctx.author.name}#{ctx.author.discriminator}) 執行指令 {ctx.message.content[1:]} 失敗'
        )


def setup(bot):
    bot.add_cog(Events(bot))
