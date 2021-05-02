import os
import discord
from discord.ext import commands
from core import CogInit, Bot, Events

import re
import random
import logging
from typing import Any
from pathlib import Path
from datetime import datetime, timedelta
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)


class EventHandlers(CogInit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.backup_path = Path(Bot.image_folder, "backup")
        self.backup_path.mkdir(exist_ok=True)

        self.ignore_list = []
        for cmd in self.bot.commands:
            self.ignore_list.append(cmd.name)
            for alias in cmd.aliases:
                self.ignore_list.append(alias)
        for word in Bot.ignore_keywords:
            self.ignore_list.append(word)

    @staticmethod
    def google_search(q: str, **kwargs) -> dict[str, Any]:
        key = Bot.google_search_api_key
        cse = Bot.custom_search_engine_id
        service = build("customsearch", "v1", developerKey=key)
        res = service.cse().list(q=q, cx=cse, **kwargs).execute()
        return res["items"]

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logger.info("Bot is ready")

        await self.bot.get_channel(
            Bot.log_channel
        ).send(f'你家機器人睡醒囉 `{datetime.now().strftime("%Y/%m/%d %H:%M:%S")}`')

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message) -> None:
        # 忽略指定頻道
        if msg.channel and msg.channel.id in Bot.ignore_channels: return

        author = msg.author
        author_name = author.display_name.lower()
        content = msg.content.lower()

        # Reaction
        if "ㄐㄐ" in content:
            await msg.add_reaction("\N{AUBERGINE}")
        if "雞雞" in content:
            await msg.add_reaction("<:emoji_101:713997954201157723>")
        if "尻尻" in content:
            await msg.add_reaction("<a:emoji_103:713998749680009250>")
        if "<:095:802993480632631316>" in content:
            await msg.reply(Events.helen_art)

        if msg.author.bot: return
        # Mentioned
        if self.bot.user in msg.mentions:
            await msg.reply(random.choice(Events.mentioned_reply))
        # 窩不知道
        elif any(kw in content for kw in ("窩不知道", "我不知道", "idk")):
            images = [i[0] for i in Events.idk]
            weights = [i[1] for i in Events.idk]

            pic = random.choices(images, weights=weights)[0]

            if pic.endswith(".gif"):
                await msg.reply(file=discord.File(pic), delete_after=20)
            else:
                await msg.reply(file=discord.File(pic), delete_after=7)
        # 讀取貓咪
        elif any(kw in content for kw in ("ldc", "痾")):
            await msg.channel.send(Events.loading_cat[0])
            await msg.channel.send(Events.loading_cat[1])
            await msg.channel.send(Events.loading_cat[2])
        # 撒嬌 (訊息)
        elif any(kw in content for kw in ("donut", "bakery", "撒嬌")):
            if random.randint(0, 4) == 4:
                await msg.reply(f"還敢撒嬌阿")
            else:
                await msg.reply(random.choice(Events.act_cute))
        # 撒嬌 (名稱)
        elif any(kw in author_name for kw in ("donut", "bakery", "撒嬌")):
            await msg.add_reaction(random.choice(Events.act_cute))
        # 好耶
        elif "好耶" in content:
            pic = discord.File(random.choice(Events.yeah))
            await msg.reply(file=pic, delete_after=5)
        # 交朋友
        elif "交朋友" in content:
            pic = discord.File(Events.make_friend)
            await msg.reply(file=pic, delete_after=10)
        # 很嗆是吧
        elif re.search(r"很嗆(?:是吧|[喔欸])?|嗆[喔欸]", content):
            pic = discord.File(Events.flaming)
            await msg.reply(file=pic, delete_after=7)
        # 請問
        if content.startswith("請問"):
            result = self.google_search(content[2:],
                                        lr="lang_zh-TW",
                                        safe="off",
                                        num=1)[0]
            await msg.reply(result["link"])

        # 圖片備份
        counter = 0
        for attachment in msg.attachments:
            if any(attachment.filename.lower().endswith(ext)
                   for ext in (".jpg", ".jpeg", ".png", ".gif")):
                counter += 1
                ext = attachment.filename.split(".")[1]
                await attachment.save(self.backup_path /
                                      Path(f"{msg.id}_{counter:02d}.{ext}"))

    @commands.Cog.listener()
    async def on_message_delete(self, msg: discord.Message) -> None:
        # 忽略機器人
        if msg.author.bot: return
        # 忽略私訊及測試群組
        if not msg.guild or msg.guild.id == Bot.test_guild: return
        # 忽略指令
        if msg.content.lower()[1:].split(' ')[0] in self.ignore_list: return

        # 無限讀取貓咪
        if any(kw in msg.content
               for kw in (Events.loading_cat[0], Events.loading_cat[1],
                          Events.loading_cat[2])):
            await msg.channel.send(Events.loading_cat[0])
            await msg.channel.send(Events.loading_cat[1])
            await msg.channel.send(Events.loading_cat[2])

        author = msg.author
        channel = msg.channel
        create_time = (msg.created_at +
                       timedelta(hours=8)).strftime("%Y/%m/%d %H:%M:%S")
        # 尋找已備份的圖片檔
        files = [
            self.backup_path / Path(f) for f in os.listdir(self.backup_path)
            if f.startswith(str(msg.id))
        ]

        await self.bot.get_channel(Bot.chat_backup_channel).send(
            f"{author.display_name} `{author.id}`｜{channel.name} `{create_time}`\n{msg.content}",
            files=[discord.File(file) for file in files])
        # 刪除圖片
        for file in files:
            os.remove(file)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction,
                              user: discord.User) -> None:
        # 取消對貓貓分屍的行為
        if any(kw in reaction.message.content
               for kw in (Events.loading_cat[0], Events.loading_cat[1],
                          Events.loading_cat[2])):
            await reaction.message.remove_reaction(reaction, user)


def setup(bot) -> None:
    bot.add_cog(EventHandlers(bot))