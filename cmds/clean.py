import discord
from discord.ext import commands
from core.classes import Cog_Ext
from core.rwFile import get_setting

import datetime

Owner = get_setting("Owner")
Traveler = get_setting("Traveler")
Bot = get_setting("Bot")

class Clean(Cog_Ext):
    @commands.command()
    async def clean(self, ctx, number: int= None):
        def predicate(msg: discord.Message) -> bool:
            return msg.author == self.bot.user

        if number == None:
            await ctx.message.delete(delay= 3)
            deleted_msg_count = len(await ctx.channel.purge(limit= None, after= datetime.datetime.now() + datetime.timedelta(days= -5), check= predicate))
            await ctx.send(f"> 已清除 {deleted_msg_count} 則 {self.bot.user.name} 的訊息", delete_after= 10)
        else:
            await ctx.message.delete(delay= 3)
            deleted_msg_count = len(await ctx.channel.purge(limit= number + 1, check= predicate))
            await ctx.send(f"> 已清除 {deleted_msg_count} 則 {self.bot.user.name} 的訊息", delete_after= 10)
            
    @commands.command()
    async def purge(self, ctx, number: int, member: discord.Member= None):
        if ctx.author == self.bot.get_user(Owner) or ctx.author == self.bot.get_user(Traveler):
            def predicate(msg: discord.Message) -> bool:
                return member == None or msg.author == member

            if member == None:
                deleted_msg_count = len(await ctx.channel.purge(limit= number + 1, check= predicate))
                await ctx.send(f"> 已清除 {deleted_msg_count - 1} 則訊息", delete_after= 3)
            else:
                DC_Member = str(member)[:-5]
                await ctx.message.delete(delay= 3)
                deleted_msg_count = len(await ctx.channel.purge(limit= number + 1, check= predicate))
                await ctx.send(f"> 已清除 {deleted_msg_count} 則 {DC_Member} 的訊息", delete_after= 10)

    @commands.command()
    async def test(self, ctx):
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '👍'

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)
        except:
            await ctx.channel.send('👎')
        else:
            await ctx.channel.send('👍')
            
def setup(bot):
    bot.add_cog(Clean(bot))