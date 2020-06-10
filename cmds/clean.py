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
            return msg == ctx.message or msg.author == self.bot.get_user(Bot)

        await ctx.channel.purge(before= datetime.datetime.now(), check= predicate)
        await ctx.message.delete()
            
    @commands.command()
    async def purge(self, ctx, number: int, member: discord.Member= None):
        if ctx.author == self.bot.get_user(Owner) or ctx.author == self.bot.get_user(Traveler):
            def predicate(msg: discord.Message) -> bool:
                return msg == ctx.message or member == None or msg.author == member

            await ctx.channel.purge(limit= number + 1, check= predicate)
            await ctx.message.delete()
            
def setup(bot):
    bot.add_cog(Clean(bot))