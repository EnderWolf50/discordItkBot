import discord
from discord.ext import commands
from core.classes import Cog_Ext
from core.rwFile import get_setting

Owner = get_setting("Owner")

class Basic(Cog_Ext):
    @commands.command()
    async def load(self, ctx, folder, extension):
        if ctx.author == self.bot.get_user(Owner):
            self.bot.load_extension(f"{folder}.{extension}")
            await ctx.message.delete()
            await ctx.send(f"**{extension}** has been loaded!", delete_after= 3)

    @commands.command()
    async def unload(self, ctx, folder, extension):
        if ctx.author == self.bot.get_user(Owner):
            self.bot.unload_extension(f"{folder}.{extension}")
            await ctx.message.delete()
            await ctx.send(f"**{extension}** has been unloaded!", delete_after= 3)

    @commands.command()
    async def reload(self, ctx, folder, extension):
        if ctx.author == self.bot.get_user(Owner):
            self.bot.reload_extension(f"{folder}.{extension}")
            await ctx.message.delete()
            await ctx.send(f"**{extension}** has been reloaded!", delete_after= 3)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Ping is {round(self.bot.latency*1000)} ms and... Pong!')

    @commands.command()
    async def help(self, ctx):
        await ctx.send("test")

def setup(bot):
    bot.add_cog(Basic(bot))