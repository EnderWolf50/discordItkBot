import discord
from discord.ext import commands
from core.classes import Cog_Ext

class Clean(Cog_Ext):
    @commands.command()
    async def clean(self, ctx, number: int):
        def predicate(msg: discord.Message) -> bool:
            return msg == ctx.message or msg.author == self.bot.get_user(710498084194484235)

        await ctx.channel.purge(limit= number + 1, check= predicate)
        await ctx.message.delete()
            
    @commands.command()
    async def purge(self, ctx, number: int, member: discord.Member= None):
        if ctx.author == self.bot.get_user(523755296242270210) or ctx.author == self.bot.get_user(590430031281651722):
            def predicate(msg: discord.Message) -> bool:
                return msg == ctx.message or member == None or msg.author == member

            await ctx.channel.purge(limit= number + 1, check= predicate)
            await ctx.message.delete()
            
def setup(bot):
    bot.add_cog(Clean(bot))