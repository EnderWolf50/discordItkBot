import discord
from discord.ext import commands
from core import CogInit, Bot, Events, Emojis

import re
import random
import logging
from typing import Any
from pathlib import Path
from itertools import cycle
from datetime import timedelta
from datetime import datetime as dt
from googleapiclient import discovery, errors

logger = logging.getLogger(__name__)


class EventHandlers(CogInit):
    def __init__(self, *args, **kwargs) -> None:
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

        self.google_search_api_keys = cycle(Bot.google_search_api_keys)

        self._sisters_last = dt.utcnow()

    def google_search(self, q: str, **kwargs) -> dict[str, Any]:
        key = next(self.google_search_api_keys)
        cse = Bot.custom_search_engine_id
        try:
            service = discovery.build("customsearch", "v1", developerKey=key)
            res = service.cse().list(q=q,
                                     cx=cse,
                                     **Bot.google_search_options,
                                     **kwargs).execute()

            return res.get("items", None)
        except errors.HttpError:
            logger.error(f"使用 {key} 進行搜索時發生錯誤，可能是超出配額或或金鑰無效")

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logger.info("Bot is ready")

        await self.bot.get_channel(
            Bot.log_channel
        ).send(f'你家機器人睡醒囉 `{dt.now().strftime("%Y/%m/%d %H:%M:%S")}`')

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

        mentions = [u.display_name for u in msg.mentions]
        # 提及機器人
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
        # 素每（訊息）
        elif any(kw in content for kw in ("熱", "好熱", "素每")):
            pic = discord.File(random.choice(Events.so_hot))
            await msg.reply(file=pic, delete_after=7)
        # 素每（提及）
        elif any("素每" in name for name in mentions):
            pic = discord.File(random.choice(Events.so_hot))
            await msg.reply(file=pic, delete_after=7)
        # 假的
        elif "假的" in content:
            pic = discord.File(Events.fake)
            await msg.reply(file=pic, delete_after=10)
        # 你很壞
        elif "你很壞" in content:
            pic = discord.File(Events.you_bad)
            await msg.reply(file=pic, delete_after=7)
        # 好耶
        elif "好耶" in content:
            pic = discord.File(random.choice(Events.yeah))
            await msg.reply(file=pic, delete_after=5)
        # 交朋友
        elif "交朋友" in content:
            pic = discord.File(Events.make_friend)
            await msg.reply(file=pic, delete_after=7)
        # 很嗆是吧
        elif re.search(r"很嗆(?:是吧|[喔欸])?|嗆[喔欸]", content):
            pic = discord.File(Events.flaming)
            await msg.reply(file=pic, delete_after=7)
        # 綺麗な双子
        # 確認最後一則訊息距離現在大於二十秒
        if dt.utcnow() - self._sisters_last >= timedelta(seconds=15):
            # 判定是否為其中一人
            _sister_1 = True if author_name == "綺麗な双子(姊)" else False
            _sister_2 = True if author_name == "綺麗な双子(妹)" else False
            # 若為其中一人則處理
            if _sister_1 or _sister_2:
                # 獲取 20 秒內的歷史訊息
                async for _m in msg.channel.history(limit=None,
                                                    after=msg.created_at -
                                                    timedelta(seconds=15.5),
                                                    oldest_first=False):
                    _m_author_name = _m.author.display_name.lower()
                    # 如果 20 秒內已經觸發過，跳過並重新記錄時間
                    if "sisters.jpg" in {_a.filename for _a in _m.attachments}:
                        self._sisters_last = dt.utcnow()
                        _sister_1 = _sister_2 = False
                        break
                    if _sister_2 and _m_author_name == "綺麗な双子(姊)":
                        _sister_1 = True
                    if _sister_1 and _m_author_name == "綺麗な双子(妹)":
                        _sister_2 = True
                    # 皆為 True 提早跳出以便發送
                    if _sister_1 and _sister_2: break
                # 皆為 True 則兩者於 20 秒內同時出現
                if _sister_1 and _sister_2:
                    # 紀錄發送時間
                    self._sisters_last = dt.utcnow()
                    pic = discord.File(Events.sisters)
                    await msg.channel.send(file=pic, delete_after=15)
        # 請問
        if content.startswith("請問"):
            if content[2:4] == "早餐":
                pass
            elif content[2:4] == "晚餐":
                await msg.reply(random.choice(Events.meals.dinner))
            else:
                result = self.google_search(content[2:], num=1)
                if result is None:
                    await msg.reply(
                        f"很遺憾\n你問的東西連 Google 都回答不了你 {Emojis.pepe_coffee}",
                        delete_after=10)
                    await msg.delete(delay=10)
                    return
                await msg.reply(result[0]["link"])

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
    async def on_message_edit(self, before: discord.Message,
                              after: discord.Message) -> None:
        # 忽略頻道
        if after.channel and after.channel.id in Bot.ignore_channels: return
        # 忽略機器人
        if after.author.bot: return
        # 忽略私訊及測試群組
        if not after.guild or after.guild.id == Bot.test_guild: return
        # 前後訊息內容相同，略過
        if before.content.lower() == after.content.lower(): return

        author = after.author
        channel = after.channel
        create_time = (after.edited_at +
                       timedelta(hours=8)).strftime("%Y/%m/%d %H:%M:%S")
        # 尋找已備份的圖片檔
        files = [
            f for f in self.backup_path.iterdir()
            if f.name.startswith(str(after.id))
        ]
        await self.bot.get_channel(Bot.edit_backup_channel).send(
            f"{author.display_name} `{author.id}`｜{channel.name} `{create_time}`\n{before.content} `→` {after.content}",
            files=[discord.File(file) for file in files])

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
            f for f in self.backup_path.iterdir()
            if f.name.startswith(str(msg.id))
        ]
        await self.bot.get_channel(Bot.chat_backup_channel).send(
            f"{author.display_name} `{author.id}`｜{channel.name} `{create_time}`\n{msg.content}",
            files=[discord.File(file) for file in files])
        # 刪除圖片
        for file in files:
            file.unlink()

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
