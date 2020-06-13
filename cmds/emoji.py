import discord
from discord.ext import commands
from core.classes import Cog_Ext

class Emoji(Cog_Ext):
    @commands.command(aliases= ["Emo"])
    async def Emoji(self, ctx, *,E_input):
        if E_input.startswith(":") and E_input.endswith(":"):
            E_input = E_input.strip(":")
        try:
            Emoji = await commands.EmojiConverter().convert(ctx, E_input)
        except:
            await ctx.send("Input error!")
        else:
            if Emoji.animated:
                await ctx.send(f"\<a:{Emoji.name}:{Emoji.id}>")
            else:
                await ctx.send(f"\<:{Emoji.name}:{Emoji.id}>")
        await ctx.message.delete(delay= 3)

def setup(bot):
    bot.add_cog(Emoji(bot))