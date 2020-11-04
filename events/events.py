import discord
from discord.ext import commands
from core.classes import Cog_Ext
from core.rwFile import rFile, get_setting

from datetime import datetime as dt
import random, re, asyncio

File = rFile('others')

idk = list(File['IDK_url'].keys())
idk_weights = list(File['IDK_url'].values())

mentionReact = File["Mention_react"]

Owner = get_setting("Owner")

yeahlist = [
    "./images/yeah.jpg", "./images/noyeah.jpg", "./images/yeahsanxiao.jpg",
    "./images/yeahstarburst.jpg", "./images/yeah_man.jpg"
]

actCute = [
    "<:102:737843533611794463>", "<:103:737846127117991986>",
    "<:104:737849572314972181>", "<:105:741919410746425416>",
    "<:106:738031132490072076>", "<:112:741919374549712947>",
    "<:113:741919392585089024>"
]

loadingCatEmos = [
    "<:ldc_01:725343128986320916><:ldc_02:725343129011486761><:ldc_03:725343129183584367><:ldc_04:725343129011748976><:ldc_05:725343128604770348>",
    "<:ldc_06:725343128910954547><:ldc_07:725343128839520259><a:ldc_08:725343129892552764><:ldc_09:725343129011617852><:ldc_10:725343128986583059>",
    "<:ldc_11:725343129087115374><:ldc_12:725343128818548737><:ldc_13:725343128822743041><:ldc_14:725343128994840657><:ldc_15:725343129003360346>"
]

voted_messages = []

au_emojis = [
    '<:AU_yellow:773465852044640286>', '<:AU_white:773465852015804446>',
    '<:AU_red:773465851969798154>', '<:AU_purple:773465851705688065>',
    '<:AU_pink:773465852283715584>', '<:AU_orange:773465851873591296>',
    '<:AU_lime:773465851809497128>', '<:AU_green:773465851717353472>',
    '<:AU_cyan:773465851713421312>', '<:AU_brown:773465851453243423>',
    '<:AU_blue:773465851709358111>', '<:AU_black:773465851634122752>'
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
        await self.bot.get_user(523755296242270210).send(
            f'Bot has been started successfully `{dt.now().strftime("%Y/%m/%d %H:%M:%S")}`'
        )

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.channel == self.bot.get_channel(675956755112394753): return
        # reaction
        if "ㄐㄐ" in msg.content:
            await msg.add_reaction("\N{AUBERGINE}")
        if "雞雞" in msg.content:
            await msg.add_reaction("<:emoji_101:713997954201157723>")
        if "尻尻" in msg.content:
            await msg.add_reaction("<a:emoji_103:713998749680009250>")
        if msg.author.id == 429992095374114826:
            await msg.add_reaction(random.choice(['🎫', '🎟️']))

        if msg.author.bot: return
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
        elif re.search(r"(ldc|ldcat|\b痾\b|\b痾...\b)", msg.content.lower()):
            await msg.channel.send(loadingCatEmos[0])
            await msg.channel.send(loadingCatEmos[1])
            await msg.channel.send(loadingCatEmos[2])
        # 好耶
        elif "好耶" in msg.content:
            pic = discord.File(random.choice(yeahlist))
            await msg.channel.send(file=pic, delete_after=15)
        # mention
        elif self.bot.user in msg.mentions and len(msg.mentions) == 1:
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
        if msg.guild.id == 725295821456801842: return
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
        if reaction.emoji in ['🎫', '🎟️']:
            if reaction.count == 3 and reaction.message.id not in voted_messages:
                voted_messages.append(reaction.message.id)
                emojis = au_emojis.copy()
                for i in range(3):
                    await reaction.message.add_reaction(
                        random.shuffle(emojis).pop())
                    await asyncio.sleep(0.5)
                msg = await reaction.message.channel.send(
                    f'''. 　　　　　。　　　　　　•　　　 　ﾟ　　。 　　.

　　　.　　　 　　　　.　　　　　　　。　　　 。　. 　

.　　 。　　               　　　  。 . 　   　    • 　　　  　 　•

　. 　ﾟ　.        {reaction.message.author.mention}   was An Impostor.　            。   　.

　   　'　　          　  0 Impostor remains      　 　　   。

　　ﾟ　　　　　.　　　　　. ,　　　　　　　　.　 .''')
                await asyncio.sleep(1)
                await msg.edit(content=f'''. 　　　　　。　　　　　　•　　　 　ﾟ　　。 　　.

　　　.　　　 　　　　.　　　　　　　。　　　 。　. 　

.　　 。　　ඞ               　　　  。 . 　     　 • 　　　   　•

　. 　ﾟ　.        {reaction.message.author.mention}  was An Impostor.　            。   　.

　   　'　　          　  0 Impostor remains      　 　　   。

　　ﾟ　　　　　.　　　　　. ,　　　　　　　　.　 .''')
                await asyncio.sleep(1)
                await msg.edit(content=f'''. 　　　　　。　　　　　　•　　　 　ﾟ　　。 　　.

　　　.　　　 　　　　.　　　　　　　。　　　 。　. 　

.　　 。　　      ඞ         　　　  。 . 　     　 • 　　　   　•

　. 　ﾟ　.        {reaction.message.author.mention}  was An Impostor.　            。   　.

　   　'　　          　  0 Impostor remains      　 　　   。

　　ﾟ　　　　　.　　　　　. ,　　　　　　　　.　 .''')
                await asyncio.sleep(1)
                await msg.edit(content=f'''. 　　　　　。　　　　　　•　　　 　ﾟ　　。 　　.

　　　.　　　 　　　　.　　　　　　　。　　　 。　. 　

.　　 。　　             ඞ  　　　  。 . 　     　 • 　　　   　•

　. 　ﾟ　.        {reaction.message.author.mention}  was An Impostor.　            。   　.

　   　'　　          　  0 Impostor remains      　 　　   。

　　ﾟ　　　　　.　　　　　. ,　　　　　　　　.　 .''')
                await asyncio.sleep(1)
                await msg.edit(content=f'''. 　　　　　。　　　　　　•　　　 　ﾟ　　。 　　.

　　　.　　　 　　　　.　　　　　　　。　　　 。　. 　

.　　 。　　               　　　 ඞ 。 . 　     　 • 　　　   　•

　. 　ﾟ　.        {reaction.message.author.mention}  was An Impostor.　            。   　.

　   　'　　          　  0 Impostor remains      　 　　   。

　　ﾟ　　　　　.　　　　　. ,　　　　　　　　.　 .''')
                await asyncio.sleep(1)
                await msg.edit(content=f'''. 　　　　　。　　　　　　•　　　 　ﾟ　　。 　　.

　　　.　　　 　　　　.　　　　　　　。　　　 。　. 　

.　　 。　　               　　　  。 . 　ඞ     　 • 　　　   　•

　. 　ﾟ　.        {reaction.message.author.mention}  was An Impostor.　            。   　.

　   　'　　          　  0 Impostor remains      　 　　   。

　　ﾟ　　　　　.　　　　　. ,　　　　　　　　.　 .''')
                await asyncio.sleep(1)
                await msg.edit(content=f'''. 　　　　　。　　　　　　•　　　 　ﾟ　　。 　　.

　　　.　　　 　　　　.　　　　　　　。　　　 。　. 　

.　　 。　　               　　　  。 . 　   　    ඞ 　　　   　.•

　. 　ﾟ　.        {reaction.message.author.mention}   was An Impostor.　            。   　.

　   　'　　          　  0 Impostor remains      　 　　   。

　　ﾟ　　　　　.　　　　　. ,　　　　　　　　.　 .''')
                await asyncio.sleep(1)
                await msg.edit(content=f'''. 　　　　　。　　　　　　•　　　 　ﾟ　　。 　　.

　　　.　　　 　　　　.　　　　　　　。　　　 。　. 　

.　　 。　　               　　　  。 . 　   　    • 　　　  ඞ 　•

　. 　ﾟ　.        {reaction.message.author.mention}   was An Impostor.　            。   　.

　   　'　　          　  0 Impostor remains      　 　　   。

　　ﾟ　　　　　.　　　　　. ,　　　　　　　　.　 .''')
                await asyncio.sleep(1)
                await msg.edit(content=f'''. 　　　　　。　　　　　　•　　　 　ﾟ　　。 　　.

　　　.　　　 　　　　.　　　　　　　。　　　 。　. 　

.　　 。　　               　　　  。 . 　   　    • 　　　  　 　•

　. 　ﾟ　.        {reaction.message.author.mention}   was An Impostor.　            。   　.

　   　'　　          　  0 Impostor remains      　 　　   。

　　ﾟ　　　　　.　　　　　. ,　　　　　　　　.　 .''',
                               delete_after=7)

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
