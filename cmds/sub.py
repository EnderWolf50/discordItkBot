import discord
from discord.ext import commands
from core.classes import Cog_Ext
from core.rwFile import rFile, wFile, get_setting

import asyncio, os, re
from redis import Redis, ConnectionPool
from datetime import datetime as dt

administrators = [
    get_setting("Owner"),
    get_setting("Traveler"),
    get_setting("Juxta")
]

host = os.environ["host"]
port = os.environ["port"]
password = os.environ["password"]

subscriberList = {}
channel = 675956755112394753

pool = ConnectionPool(host=host, port=port, password=password)


class Subscribe(Cog_Ext):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        async def autoRefreshList():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                await listRefreshFunc()
                print(" ")
                print(dt.now().strftime('%m/%d %H:%M:%S'))
                print(f"autoRefreshList >> Complete")
                print(" ")
                await asyncio.sleep(900)

        self.autoRefreshListTask = self.bot.loop.create_task(autoRefreshList())

        async def autoRefreshMsgEmbed():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                await asyncio.sleep(20)
                await refreshMsgEmbedFunc(self)
                print(" ")
                print(dt.now().strftime('%m/%d %H:%M:%S'))
                print(f"autoRefreshMsgEmbed >> Complete")
                print(" ")
                await asyncio.sleep(900)

        self.autoRefreshMsgEmbedTask = self.bot.loop.create_task(
            autoRefreshMsgEmbed())

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.channel != self.bot.get_channel(channel) or msg.author.bot: return
        if re.search(r"^(\.(subscriber|sub|s))\b", msg.content.lower()): return
        if len(msg.mentions) == 0: return

        await msg.delete(delay=5)
        try:
            r = Redis(connection_pool=pool)

            for user in msg.mentions:
                if f"{user.id}" not in subscriberList.keys(): continue
                timestamp = "".join(subscriberList[f"{user.id}_time"])

                subscriptionInfo = f"<@{user.id}>\n"
                for value in subscriberList[f"{user.id}"]:
                    subscriptionInfo += f"> {value}\n"
                subscriptionInfo += f"`最後編輯：{timestamp}`"

                if re.search(r"\b(b|bind|bound)$", msg.content.lower()) and msg.author.id in administrators:
                    msgSent = await msg.channel.send(subscriptionInfo)

                    r.set(f"{user.id}_msg", msgSent.id)
                    subscriberList[f"{user.id}_msg"] = [str(msgSent.id)]

                    r.set(f"{user.id}_msg_channel", msgSent.channel.id)
                    subscriberList[f"{user.id}_msg_channel"] = [str(msgSent.channel.id)]
                else:
                    await msg.channel.send(subscriptionInfo, delete_after=45)
        except:
            await ctx.send('There something went wrong while processing the message.', delete_after=5)
        finally:
            pool.disconnect()

    @commands.group(aliases=['s', 'sub'])
    async def subscriber(self, ctx):
        await ctx.message.delete(delay=5)

    @subscriber.command(aliases=['l'])
    async def list(self, ctx):
        if ctx.channel != self.bot.get_channel(channel) or ctx.author.id not in administrators: return

        try:
            r = Redis(connection_pool=pool)
            subscriberListCopy = subscriberList.copy()

            for key, value in subscriberListCopy.items():
                if re.search(r"(_embed|_msg|_channel|_time)$", key): continue
                timestamp = "".join(subscriberList[f"{key}_time"])

                listMsg = f"<@{key}>\n"
                for line in value:
                    listMsg += f"> {line}\n"
                listMsg += f"`最後編輯：{timestamp}`"

                if re.search(r"\b(b|bind|bound)$", ctx.message.content.lower()):
                    msg = await ctx.channel.send(listMsg)

                    r.set(f"{key}_msg", msg.id)
                    subscriberList[f"{key}_msg"] = [str(msg.id)]

                    r.set(f"{key}_msg_channel", msg.channel.id)
                    subscriberList[f"{key}_msg_channel"] = [str(msg.channel.id)]
                else:
                    await ctx.channel.send(listMsg, delete_after=45)
        except:
            await ctx.send("There is something went wrong while processing the command.", delete_after=5)
        finally:
            pool.disconnect()

    @subscriber.command(aliases=['lr', 'reload', 'refresh', 'listReload'])
    async def listRefresh(self, ctx):
        if ctx.author.id not in administrators: return

        try:
            await listRefreshFunc()
        except:
            await ctx.send("There is something went wrong while processing the command.", delete_after=5)
        else:
            await ctx.channel.send('List refresh complete.', delete_after=5)
        finally:
            pool.disconnect()

    @subscriber.command(aliases=['s'])
    async def set(self, ctx, user: discord.Member = None, *args):
        if ctx.author.id not in administrators: return
        if user == None or not args: return

        try:
            r = Redis(connection_pool=pool)
            newSubscriptionInfo = ", ".join(args)

            r.set(f"{user.id}", newSubscriptionInfo)
            subscriberList[f"{user.id}"] = newSubscriptionInfo.split(", ")

            r.set(f"{user.id}_time", dt.now().strftime('%m/%d %H:%M:%S'))
            subscriberList[f"{user.id}_time"] = [dt.now().strftime('%m/%d %H:%M:%S')]
        except:
            await ctx.send('There something went wrong while processing the command.', delete_after=5)
        else:
            infoMsg = f'New subscription info of `{user.name}` will be looked like:\n{user.mention}'

            for arg in args:
                infoMsg += f"\n{arg}"
            await ctx.send(infoMsg, delete_after=10)

            if f"{user.id}_embed" in subscriberList.keys():
                await refreshEmbed(self, user)
            if f"{user.id}_msg" in subscriberList.keys():
                await refreshMsg(self, user)
        finally:
            pool.disconnect()

    @subscriber.command(aliases=['d', 'del'])
    async def delete(self, ctx, user: discord.Member = None):
        if ctx.author.id not in administrators: return
        if user == None: return

        try:
            r = Redis(connection_pool=pool)

            r.delete(f"{user.id}")
            r.delete(f"{user.id}_time")

            r.delete(f"{user.id}_embed")
            r.delete(f"{user.id}_embed_channel")

            r.delete(f"{user.id}_msg")
            r.delete(f"{user.id}_msg_channel")

            if f"{user.id}" in subscriberList.keys():
                del subscriberList[f"{user.id}"]
        except:
            await ctx.send(
                'There something went wrong while processing the command.',
                delete_after=5)
        else:
            await ctx.send(
                f'Subscription info of {user.mention} has been removed successfully.',
                delete_after=7)

            if f"{user.id}_embed" in subscriberList.keys():
                await deleteEmbed(self, user)
            if f"{user.id}_msg" in subscriberList.keys():
                await deleteMsg(self, user)
            if f"{user.id}_time" in subscriberList.keys():
                del subscriberList[f"{user.id}_time"]
        finally:
            pool.disconnect()

    @subscriber.command(aliases=['a'])
    async def add(self, ctx, user: discord.Member, *args):
        if ctx.author.id not in administrators: return
        if user == None or not args: return

        try:
            r = Redis(connection_pool=pool)
            newSubscriptionInfo = f"{r.get(f'{user.id}').decode('utf-8')}, {', '.join(args)}"

            r.set(f"{user.id}", newSubscriptionInfo)
            subscriberList[f"{user.id}"] = newSubscriptionInfo.split(', ')

            r.set(f"{user.id}_time", dt.now().strftime('%m/%d %H:%M:%S'))
            subscriberList[f"{user.id}_time"] = [dt.now().strftime('%m/%d %H:%M:%S')]
        except:
            await ctx.send(
                'There something went wrong while processing the command.',
                delete_after=5)
        else:
            infoMsg = f'New subscription info of `{user.name}` will be looked like:\n{user.mention}'

            for arg in subscriberList[f"{user.id}"]:
                infoMsg += f"\n{arg}"
            await ctx.send(infoMsg, delete_after=10)

            if f"{user.id}_embed" in subscriberList.keys():
                await refreshEmbed(self, user)
            if f"{user.id}_msg" in subscriberList.keys():
                await refreshMsg(self, user)
        finally:
            pool.disconnect()

    @subscriber.command(aliases=['r', 're'])
    async def remove(self, ctx, user: discord.Member, line: int):
        if ctx.author.id not in administrators: return
        if user == None or not line: return

        try:
            r = Redis(connection_pool=pool)
            uneditedInfo = r.get(f'{user.id}').decode('utf-8').split(', ')
            lineRemoved = uneditedInfo.pop(line - 1)
            newSubscriptionInfo = ", ".join(uneditedInfo)

            r.set(f"{user.id}", newSubscriptionInfo)
            subscriberList[f"{user.id}"] = newSubscriptionInfo.split(', ')

            r.set(f"{user.id}_time", dt.now().strftime('%m/%d %H:%M:%S'))
            subscriberList[f"{user.id}_time"] = [dt.now().strftime('%m/%d %H:%M:%S')]
        except:
            await ctx.send(
                'There something went wrong while processing the command.',
                delete_after=5)
        else:
            infoMsg = f'New subscription info of `{user.name}` will be looked like:\n{user.mention}'

            for arg in subscriberList[f"{user.id}"]:
                infoMsg += f"\n{arg}"
            await ctx.send(infoMsg, delete_after=10)

            if f"{user.id}_embed" in subscriberList.keys():
                await refreshEmbed(self, user)
            if f"{user.id}_msg" in subscriberList.keys():
                await refreshMsg(self, user)
        finally:
            pool.disconnect()

    @subscriber.command(aliases=['e'])
    async def embed(self, ctx, user: discord.Member = None, color="BAD9A2"):
        if ctx.author.id not in administrators: return
        if user == None: return
        if f"{user.id}" not in subscriberList.keys(): return
        if len(color) != 6: color = "BAD9A2"

        try:
            description = ""
            timestamp = "".join(subscriberList[f"{user.id}_time"])

            for value in subscriberList[f"{user.id}"]:
                description += f"{value}\n"

            embed = discord.Embed(description=description, color=int(color, 16))
            embed.set_author(name=user.name, icon_url=user.avatar_url)
            embed.set_footer(text= f"最後編輯：{timestamp}")

            msg = await ctx.send(embed=embed)
            if re.search(r"\b(b|bind|bound)$", ctx.message.content.lower()):
                r = Redis(connection_pool=pool)

                r.set(f"{user.id}_embed", msg.id)
                subscriberList[f"{user.id}_embed"] = [str(msg.id)]

                r.set(f"{user.id}_embed_channel", msg.channel.id)
                subscriberList[f"{user.id}_embed_channel"] = [str(msg.channel.id)]
        except:
            await ctx.send("There is something went wrong while processing the command.", delete_after=5)
        finally:
            pool.disconnect()

    @subscriber.command(aliases=['ea'])
    async def embedAll(self, ctx, color="BAD9A2"):
        # if ctx.channel != self.bot.get_channel(channel): return
        if ctx.author.id not in administrators: return

        try:
            r = Redis(connection_pool=pool)
            subscriberListCopy = subscriberList.copy()

            if len(color) != 6: color = "BAD9A2"

            for key, value in subscriberListCopy.items():
                if re.search(r"(_embed|_msg|_channel|_time)$", key): continue
                description = ""
                user = self.bot.get_user(int(key))
                timestamp = "".join(subscriberList[f"{user.id}_time"])

                for line in value:
                    description += f"{line}\n"

                embed = discord.Embed(description=description, color=int(color, 16))
                embed.set_author(name=user.name, icon_url=user.avatar_url)
                embed.set_footer(text= f"最後編輯：{timestamp}")

                msg = await ctx.send(embed=embed)
                if re.search(r"\b(b|bind|bound)$", ctx.message.content.lower()):
                    r.set(f"{user.id}_embed", msg.id)
                    subscriberList[f"{user.id}_embed"] = [str(msg.id)]

                    r.set(f"{user.id}_embed_channel", msg.channel.id)
                    subscriberList[f"{user.id}_embed_channel"] = [str(msg.channel.id)]
        except:
            await ctx.send("There is something went wrong while processing the command.", delete_after=5)
        finally:
            pool.disconnect()

    @subscriber.command(aliases=['i'])
    async def info(self, ctx, user: discord.Member = None):
        if ctx.channel != self.bot.get_channel(channel): return
        if ctx.author.id not in administrators: return
        if user == None: return

        if len(ctx.message.mentions) == 1 and str(
                ctx.message.mentions[0].id) in subscriberList.keys():
            await ctx.message.delete(delay=5)

            subscriptionInfo = f"<@{ctx.message.mentions[0].id}>"
            for value in subscriberList[f"{ctx.message.mentions[0].id}"]:
                subscriptionInfo += f"\n{value}"

            await ctx.send(subscriptionInfo)

    @subscriber.command(aliases=['h'])
    async def help(self, ctx):
        if ctx.author.id not in administrators: return
        description = '''
於 <#675956755112394753> Tag 人（可複數）可查詢訂閱現況
* 管理者於最後打上 `b|bind|bound` 可使訊息不消失且綁定

主指令:
`s|sub|subscriber <子指令>`

子指令:
`set|s <Tag 人> <內容...>` 設定訂閱資訊
* 內容有空格時用 "" 框起即可被視為單項

`add|a <Tag 人> <內容...>` 增加訂閱資訊
* 內容有空格時用 "" 框起即可被視為單項

`remove|re|r <Tag 人> <行數>` 移除指定行數

`delete|del|d <Tag 人>` 刪除指定訂閱者

`bound|b <Tag 人> <訊息 ID>` 綁定訂閱者訊息（嵌入與普通訊息各一）

`embed|e <Tag 人> (色碼)` 以嵌入方式呈現訂閱資訊
* 管理者於最後打上 `b|bind|bound` 可使訊息綁定

`embedAll|ea (色碼)` 以嵌入方式呈現所有訂閱資訊
* 管理者於最後打上 `b|bind|bound` 可使訊息綁定

`list|l` 列出所有訂閱資訊
* 管理者於最後打上 `b|bind|bound` 可使訊息不消失且綁定

`listRefresh|reload|lr` 刷新訂閱資訊（不會自動列出）
* 預設每 15 min 自動更新資訊

`info|i <Tag 人>` 以訊息方式呈現訂閱資訊（不會消失）
'''

        embed = discord.Embed(title="SubscribeInfo Command Help", description=description, color=0x7a9e7e)
        embed.set_author(name="Itk Bot", icon_url="https://cdn.discordapp.com/avatars/710498084194484235/e91dbe68bd05239c050805cc060a34e9.webp?size=128")
        await ctx.send(embed=embed)

    @subscriber.command(aliases=["b", "bind"])
    async def bound(self,  ctx, user: discord.Member = None, msg: discord.Message = None):
        if ctx.author.id not in administrators: return
        if user == None or msg == None: return
        if msg.author != self.bot.user: return

        try:
            if len(msg.embeds) == 1:
                r = Redis(connection_pool=pool)

                r.set(f"{user.id}_embed", msg.id)
                subscriberList[f"{user.id}_embed"] = [str(msg.id)]

                r.set(f"{user.id}_embed_channel", ctx.channel.id)
                subscriberList[f"{user.id}_embed_channel"] = [str(ctx.channel.id)]

                embed = discord.Embed(description=f"[Link to the message here]({msg.jump_url})", color=0xBAD9A2)
                await ctx.send(f"`Embed` bounding successful", embed=embed, delete_after=30)
            else:
                r = Redis(connection_pool=pool)

                r.set(f"{user.id}_msg", msg.id)
                subscriberList[f"{user.id}_msg"] = [str(msg.id)]

                r.set(f"{user.id}_msg_channel", ctx.channel.id)
                subscriberList[f"{user.id}_msg_channel"] = [str(ctx.channel.id)]

                embed = discord.Embed(description=f"[Link to the message here]({msg.jump_url})", color=0xBAD9A2)
                await ctx.send(f"`Msg` bounding successful", embed=embed, delete_after=30)
        except:
            await ctx.send("There is something went wrong while processing the command.", delete_after=5)
        finally:
            pool.disconnect()

async def refreshEmbed(self, user):
    msgID = "".join(subscriberList[f"{user.id}_embed"])
    channelID = "".join(subscriberList[f"{user.id}_embed_channel"])
    timestamp = "".join(subscriberList[f"{user.id}_time"])

    channel = self.bot.get_channel(int(channelID))
    msg = await channel.fetch_message(int(msgID))
    embed = msg.embeds[0]

    embed.description = "\n".join(subscriberList[f"{user.id}"])
    embed.set_author(name=user.name, icon_url=user.avatar_url)
    embed.set_footer(text= f"最後編輯：{timestamp}")
    await msg.edit(embed=embed)

async def refreshMsg(self, user):
    msgID = "".join(subscriberList[f"{user.id}_msg"])
    channelID = "".join(subscriberList[f"{user.id}_msg_channel"])
    timestamp = "".join(subscriberList[f"{user.id}_time"])

    channel = self.bot.get_channel(int(channelID))
    msg = await channel.fetch_message(int(msgID))

    msg.content = f"<@{user.id}>\n> " + "\n> ".join(subscriberList[f"{user.id}"]) + f"\n`{timestamp}`"
    await msg.edit(content=msg.content)

async def refreshMsgEmbedFunc(self):
    for key in subscriberList.keys():
        if re.search(r"(_embed)$", key):
            user = self.bot.get_user(int(key[:18]))

            await refreshEmbed(self, user)
        elif re.search(r"(_msg)$", key):
            user = self.bot.get_user(int(key[:18]))

            await refreshMsg(self, user)


async def deleteEmbed(self, user):
    msgID = "".join(subscriberList[f"{user.id}_embed"])
    channelID = "".join(subscriberList[f"{user.id}_embed_channel"])

    channel = self.bot.get_channel(int(channelID))
    msg = await channel.fetch_message(msgID)

    if f"{user.id}_embed" in subscriberList.keys():
        del subscriberList[f"{user.id}_embed"]
    if f"{user.id}_embed_channel" in subscriberList.keys():
        del subscriberList[f"{user.id}_embed_channel"]
    await msg.delete()


async def deleteMsg(self, user):
    msgID = "".join(subscriberList[f"{user.id}_msg"])
    channelID = "".join(subscriberList[f"{user.id}_msg_channel"])

    channel = self.bot.get_channel(int(channelID))
    msg = await channel.fetch_message(msgID)

    if f"{user.id}_msg" in subscriberList.keys():
        del subscriberList[f"{user.id}_msg"]
    if f"{user.id}_msg_channel" in subscriberList.keys():
        del subscriberList[f"{user.id}_msg_channel"]
    await msg.delete()


async def listRefreshFunc():
    global subscriberList
    subscriberList = {}
    r = Redis(connection_pool=pool)
    for key in r.keys():
        subscriberList[key.decode("utf-8")] = r.get(key).decode("utf-8").split(", ")
    pool.disconnect()


def setup(bot):
    bot.add_cog(Subscribe(bot))