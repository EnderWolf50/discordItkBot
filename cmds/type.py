import discord
from discord.ext import commands
from core.classes import Cog_Ext
import asyncio

class Type(Cog_Ext):
    @commands.command()
    async def Type(self, ctx, *args):
        test = list(args)
        await ctx.message.delete()
        msg = await ctx.send("** **")
        for i in test:
            await asyncio.sleep(1)
            await msg.edit(content= i)
        await msg.delete(delay= 5)
        
    @commands.command()
    async def Mconvert(self, ctx, ID):
        Member = await commands.MemberConverter().convert(ctx, ID)
        await ctx.send(Member)
        await ctx.send(Member.status)
        #await ctx.send("Y")
        #await ctx.send("N")

def setup(bot):
    bot.add_cog(Type(bot))