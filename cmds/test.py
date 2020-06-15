import discord
from discord.ext import commands
from core.classes import Cog_Ext

class Test(Cog_Ext):
    @commands.command()
    async def test(self, ctx, emoji: discord.PartialEmoji):
        if emoji.is_custom_emoji():
            await ctx.send(f"{emoji.name} {emoji.id}")
        elif emoji.is_unicode_emoji():
            await ctx.send(f"{emoji.name} {emoji.animated}")
    
    
def setup(bot):
    bot.add_cog(Test(bot))