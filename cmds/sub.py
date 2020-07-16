import discord
from discord.ext import commands
from core.classes import Cog_Ext
from core.rwFile import rFile, wFile, get_setting

import asyncio, os
from redis import Redis, ConnectionPool

administrators = [get_setting("Owner"), get_setting("Traveler"), get_setting("Juxta")]

subscriberList = {}
channel = 675956755112394753

pool = ConnectionPool(host=os.environ["host"],
                      port=os.environ["port"],
                      password=os.environ["password"])

class Subscribe(Cog_Ext):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        async def listAutoRefresh():
            await self.bot.wait_until_ready()
            global subscriberList
            while not self.bot.is_closed():
                subscriberList = {}
                r = Redis(connection_pool=pool)
                for key in r.keys():
                    subscriberList[key.decode("utf-8")] = r.get(key).decode("utf-8").split(
                        ", ")
                pool.disconnect()
                await asyncio.sleep(900)

        self.listAutoRefreshTask = self.bot.loop.create_task(listAutoRefresh())

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.channel == self.bot.get_channel(
                channel) and not msg.author.bot:
            if msg.content.startswith('.subscriber') or msg.content.startswith('.sub') or msg.content.startswith('.s'): return
            if len(msg.mentions) == 1 and str(
                    msg.mentions[0].id) in subscriberList.keys():
                await msg.delete(delay=5)

                subscriptionInfo = f"<@{msg.mentions[0].id}>"
                for value in subscriberList[f"{msg.mentions[0].id}"]:
                    subscriptionInfo += f"\n{value}"

                await msg.channel.send(subscriptionInfo, delete_after=60)

    @commands.group(aliases=['s', 'sub'])
    async def subscriber(self, ctx):
        await ctx.message.delete(delay= 5)

    @subscriber.command(aliases= ['i'])
    async def info(self, ctx, user: discord.Member= None):
        if ctx.channel != self.bot.get_channel(channel): return
        if user == None: return

        if len(ctx.message.mentions) == 1 and str(
                ctx.message.mentions[0].id) in subscriberList.keys():
            await ctx.message.delete(delay=5)

            subscriptionInfo = f"<@{ctx.message.mentions[0].id}>"
            for value in subscriberList[f"{ctx.message.mentions[0].id}"]:
                subscriptionInfo += f"\n{value}"

            await ctx.send(subscriptionInfo)

    @subscriber.command(aliases= ['e'])
    async def embed(self, ctx, user: discord.Member = None, color= "202225"):
        if ctx.author.id not in administrators: return
        if user == None: return
        if str(user.id) not in subscriberList.keys(): return

        description = ""
        for value in subscriberList[str(user.id)]:
            description += f"{value}\n"

        embed = discord.Embed(description= description, color= int(color, 16))
        embed.set_author(name= user.name, icon_url= user.avatar_url)
        await ctx.send(embed= embed)

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
        if ctx.channel != self.bot.get_channel(channel): return
        if ctx.author.id not in administrators: return
        subscriberList = {}

        try:
            r = Redis(connection_pool=pool)
            for key in r.keys():
                subscriberList[key.decode("utf-8")] = r.get(key).decode("utf-8").split(
                    ", ")
            listMsg = ""
            for k, v in subscriberList.items():
                listMsg += f"<@{k}>\n"
                for line in v:
                    listMsg += f"{line}\n"
        except:
            await ctx.send(
                'There something went wrong while using this command.', delete_after=5)
        else:
            await ctx.channel.send(listMsg, delete_after=60)
        finally:
            pool.disconnect()

    @subscriber.command(aliases= ['s'])
    async def set(self, ctx, user: discord.Member = None, *args):
        if ctx.author.id not in administrators: return
        if user == None or not args: return

        newSubscriptionInfo = ", ".join(args)
        try:
            r = Redis(connection_pool=pool)
            r.set(user.id, newSubscriptionInfo)
            subscriberList[str(user.id)] = newSubscriptionInfo.split(", ")
        except:
            await ctx.send(
                'There something went wrong while using this command.', delete_after=5)
        else:
            infoMsg = f'New subscription info of `{user.name}` will be looked like:\n{user.mention}'
            for arg in args:
                infoMsg += f"\n{arg}"
            await ctx.send(infoMsg, delete_after=10)
        finally:
            pool.disconnect()

    @subscriber.command(aliases= ['r', 're', 'del', 'delete'])
    async def remove(self, ctx, user: discord.Member = None):
        if ctx.author.id not in administrators: return
        if user == None: return

        try:
            r = Redis(connection_pool=pool)
            r.delete(user.id)
            if str(user.id) in subscriberList.keys():
                del subscriberList[str(user.id)]
        except:
            await ctx.send(
                'There something went wrong while using this command.', delete_after=5)
        else:
            await ctx.send(f'Subscription info of {user.mention} has been removed successfully.', delete_after=7)
        finally:
            pool.disconnect()


def setup(bot):
    bot.add_cog(Subscribe(bot))