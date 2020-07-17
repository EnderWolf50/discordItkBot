import discord
from discord.ext import commands
from core.classes import Cog_Ext
from core.rwFile import rFile, wFile, get_setting

import asyncio, os, re
from redis import Redis, ConnectionPool

administrators = [get_setting("Owner"), get_setting("Traveler"), get_setting("Juxta")]

host = "redis-16578.c56.east-us.azure.cloud.redislabs.com"#os.environ["host"]
port = "16578"#os.environ["port"]
password = "wPlVgO9HWu21Cs96GWnWUO29xvMtBV50"#os.environ["password"]

subscriberList = {}
channel = 675956755112394753

pool = ConnectionPool(host=host,
                      port=port,
                      password=password)

class Subscribe(Cog_Ext):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        async def listAutoRefresh():
            await self.bot.wait_until_ready()
            while not self.bot.is_closed():
                listRefreshFunc()
                pool.disconnect()
                await asyncio.sleep(900)

        self.listAutoRefreshTask = self.bot.loop.create_task(listAutoRefresh())

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.channel != self.bot.get_channel(channel) or msg.author.bot: return
        if re.search(r"^(\.(subscriber|sub|s))\b", msg.content.lower()): return
        if len(msg.mentions) == 0: return

        await msg.delete(delay=5)
        for user in msg.mentions:
            if f"{user.id}" not in subscriberList.keys(): continue
            subscriptionInfo = f"<@{user.id}>"
            for value in subscriberList[f"{user.id}"]:
                subscriptionInfo += f"\n{value}"

            if re.search(r"\b(f|forever)$", msg.content.lower()) and msg.author.id in administrators:
                await msg.channel.send(subscriptionInfo)
            else:
                await msg.channel.send(subscriptionInfo, delete_after=45)

    @commands.group(aliases=['s', 'sub'])
    async def subscriber(self, ctx):
        await ctx.message.delete(delay= 5)

    @subscriber.command(aliases= ['l'])
    async def list(self, ctx):
        if ctx.channel != self.bot.get_channel(channel): return

        listMsg = ""
        for k, v in subscriberList.items():
            listMsg += f"<@{k}>\n"
            for line in v:
                listMsg += f"{line}\n"
        await ctx.channel.send(listMsg, delete_after= 60)

    @subscriber.command(aliases= ['lr', 'reload', 'refresh', 'listReload'])
    async def listRefresh(self, ctx):
        if ctx.author.id not in administrators: return

        try:
            listRefreshFunc()
        except:
            await ctx.send(
                "There is something went wrong while processing the command.", delete_after=5)
        else:
            await ctx.channel.send('List refresh complete.', delete_after=5)
        finally:
            pool.disconnect()

    @subscriber.command(aliases= ['s'])
    async def set(self, ctx, user: discord.Member = None, *args):
        if ctx.author.id not in administrators: return
        if user == None or not args: return

        newSubscriptionInfo = ", ".join(args)
        try:
            r = Redis(connection_pool=pool)
            r.set(f"{user.id}", newSubscriptionInfo)
            subscriberList[f"{user.id}"] = newSubscriptionInfo.split(", ")
        except:
            await ctx.send(
                'There something went wrong while processing the command.', delete_after=5)
        else:
            infoMsg = f'New subscription info of `{user.name}` will be looked like:\n{user.mention}'

            for arg in args:
                infoMsg += f"\n{arg}"
            await ctx.send(infoMsg, delete_after=10)

            if f"{user.id}_msg" in subscriberList.keys():
                await refreshMsg(ctx, user)
            else:
                print('no')
        finally:
            pool.disconnect()

    @subscriber.command(aliases= ['d', 'del'])
    async def delete(self, ctx, user: discord.Member = None):
        if ctx.author.id not in administrators: return
        if user == None: return

        try:
            r = Redis(connection_pool=pool)
            r.delete(f"{user.id}")
            r.delete(f"{user.id}_msg")
            if f"{user.id}" in subscriberList.keys():
                del subscriberList[f"{user.id}"]
        except:
            await ctx.send(
                'There something went wrong while processing the command.', delete_after=5)
        else:
            await ctx.send(f'Subscription info of {user.mention} has been removed successfully.', delete_after=7)

            if f"{user.id}_msg" in subscriberList.keys():
                await deleteMsg(ctx, user)
        finally:
            pool.disconnect()

    @subscriber.command(aliases= ['a'])
    async def add(self, ctx, user: discord.Member, *args):
        if ctx.author.id not in administrators: return
        if user == None or not args: return

        try:
            r = Redis(connection_pool=pool)
            newSubscriptionInfo = f"{r.get(f"{user.id}").decode('utf-8')}, {', '.join(args)}"

            r.set(f"{user.id}", newSubscriptionInfo)
            subscriberList[f"{user.id}"] = newSubscriptionInfo.split(', ')
        except:
            await ctx.send('There something went wrong while processing the command.', delete_after=5)
        else:
            infoMsg = f'New subscription info of `{user.name}` will be looked like:\n{user.mention}'

            for arg in subscriberList[f"{user.id}"]:
                infoMsg += f"\n{arg}"
            await ctx.send(infoMsg, delete_after=10)

            if f"{user.id}_msg" in subscriberList.keys():
                await refreshMsg(ctx, user)
        finally:
            pool.disconnect()

    @subscriber.command(aliases= ['r', 're'])
    async def remove(self, ctx, user: discord.Member, line: int):
        if ctx.author.id not in administrators: return
        if user == None or not line: return

        try:
            r = Redis(connection_pool=pool)
            uneditedInfo = r.get(f"{user.id}").decode('utf-8').split(', ')
            lineRemoved = uneditedInfo.pop(line - 1)
            newSubscriptionInfo = ", ".join(uneditedInfo)

            r.set(f"{user.id}", newSubscriptionInfo)
            subscriberList[f"{user.id}"] = newSubscriptionInfo.split(', ')
        except:
            await ctx.send(
                'There something went wrong while processing the command.',
                delete_after=5)
        else:
            infoMsg = f'New subscription info of `{user.name}` will be looked like:\n{user.mention}'

            for arg in subscriberList[f"{user.id}"]:
                infoMsg += f"\n{arg}"
            await ctx.send(infoMsg, delete_after=10)

            if f"{user.id}_msg" in subscriberList.keys():
                await refreshMsg(ctx, user)
        finally:
            pool.disconnect()

    @subscriber.command(aliases= ['e'])
    async def embed(self, ctx, user: discord.Member = None, color="485696"):
        if ctx.author.id not in administrators: return
        if user == None: return
        if f"{user.id}" not in subscriberList.keys(): return

        description = ""
        for value in subscriberList[f"{user.id}"]:
            description += f"{value}\n"

        embed = discord.Embed(description= description, color= int(color, 16))
        embed.set_author(name= user.name, icon_url= user.avatar_url)
        await ctx.send(embed= embed)

    @subscriber.command(aliases= ['ea'])
    async def embedAll(self, ctx, color="485696"):
        if ctx.channel != self.bot.get_channel(channel): return
        if ctx.author.id not in administrators: return

        for key, value in subscriberList.items():
            description = ""
            user = self.bot.get_user(int(key))
            for line in value:
                description += f"{line}\n"
            embed = discord.Embed(description= description, color= int(color, 16))
            embed.set_author(name=user.name, icon_url=user.avatar_url)
            await ctx.send(embed=embed)

    @subscriber.command(aliases= ['i'])
    async def info(self, ctx, user: discord.Member= None):
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

    @subscriber.command(aliases= ['h'])
    async def help(self, ctx):
        if ctx.author.id not in administrators: return
        description = '''
在 <#675956755112394753> Tag 人（可複數）即可查詢訂閱現況
* 管理者於最後打上 f|forever 可使訊息不消失

主指令:
`s|sub|subscriber <子指令>`

子指令:
`set|s <Tag 人> <內容...>` 設定訂閱資訊
* 內容有空格時可用 "" 包起即會視為一項

`add|a <Tag 人> <內容...>` 增加訂閱資訊
* 內容有空格時可用 "" 包起即會視為一項

`remove|re|r <Tag 人> <行數>` 移除指定行數

`delete|del|d <Tag 人>` 刪除指定訂閱者

`embed|e <Tag 人> (色碼)` 以嵌入方式呈現訂閱資訊

`embedAll|ea (色碼)` 以嵌入方式呈現所有訂閱資訊

`list|l` 列出所有訂閱資訊

`listRefresh|reload|lr` 刷新訂閱資訊（不會自動列出）
* 預設每 15 min 會自動更新資訊

`info|i <Tag 人>` 以訊息方式呈現訂閱資訊（不會消失）
'''

        embed = discord.Embed(title="SubscribeInfo Command Help",
                              description=description,
                              color=0x7a9e7e)
        embed.set_author(name= "Itk Bot", icon_url= "https://cdn.discordapp.com/avatars/710498084194484235/e91dbe68bd05239c050805cc060a34e9.webp?size=128")
        await ctx.send(embed= embed)

    @subscriber.command(aliases= ["b"])
    async def bound(self, ctx, user: discord.Member= None, msg: discord.Message= None):
        if ctx.author.id not in administrators: return
        if user == None or msg == None: return
        if msg.author != self.bot.user: return

        try:
            r = Redis(connection_pool=pool)
            r.set(f"{user.id}_msg", msg.id)
            subscriberList[f"{user.id}_msg"] = [str(msg.id)]
        except:
            await ctx.send("There is something went wrong while processing the command.", delete_after= 5)
        else:
            await ctx.send(msg.jump_url)
        finally:
            pool.disconnect()

    @subscriber.command()
    async def test(self, ctx, user: discord.Member):
        await ctx.send(subscriberList.keys())


async def refreshMsg(ctx, user):
    msgID = "".join(subscriberList[f"{user.id}_msg"])

    msg = await ctx.fetch_message(msgID)
    embed = msg.embeds[0]

    embed.description = "\n".join(subscriberList[f"{user.id}"])
    await msg.edit(embed= embed)

async def deleteMsg(ctx, user):
    msgID = "".join(subscriberList[f"{user.id}_msg"])

    msg = await ctx.fetch_message(msgID)

    if f"{user.id}_msg" in subscriberList.keys():
        del subscriberList[f"{user.id}_msg"]
    await msg.delete()

def listRefreshFunc():
    global subscriberList
    subscriberList = {}
    r = Redis(connection_pool=pool)
    for key in r.keys():
        subscriberList[key.decode("utf-8")] = r.get(key).decode("utf-8").split(", ")
    print(subscriberList.keys())

def setup(bot):
    bot.add_cog(Subscribe(bot))