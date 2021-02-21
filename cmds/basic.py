import discord
from discord.ext import commands
from core.classes import Cog_Ext
from core.rwFile import get_setting, rFile

import random

Owner = get_setting("Owner")
from datetime import datetime as dt


class Basic(Cog_Ext):
    @commands.command()
    async def load(self, ctx, folder, extension):
        if ctx.author == self.bot.get_user(Owner):
            self.bot.load_extension(f"{folder}.{extension}")
            await ctx.message.delete()
            await ctx.send(f"**{extension}** has been loaded!", delete_after=3)

    @commands.command()
    async def unload(self, ctx, folder, extension):
        if ctx.author == self.bot.get_user(Owner):
            self.bot.unload_extension(f"{folder}.{extension}")
            await ctx.message.delete()
            await ctx.send(f"**{extension}** has been unloaded!",
                           delete_after=3)

    @commands.command()
    async def reload(self, ctx, folder, extension):
        if ctx.author == self.bot.get_user(Owner):
            self.bot.reload_extension(f"{folder}.{extension}")
            await ctx.message.delete()
            await ctx.send(f"**{extension}** has been reloaded!",
                           delete_after=3)

    @commands.command()
    async def help(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title="看看是哪個小可憐忘記指令怎麼打啦？", color=0xFCD992)
        embed.set_author(
            name="Itk Bot",
            icon_url=
            "https://cdn.discordapp.com/avatars/710498084194484235/e91dbe68bd05239c050805cc060a34e9.webp?size=128"
        )
        embed.set_footer(text="那個...窩不知道")
        for command, description, inline in rFile("others")["help"]:
            embed.add_field(name=command, value=description, inline=inline)
        await ctx.send(embed=embed, delete_after=30)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(round(self.bot.latency * 1000))

    @commands.command()
    async def test(self, ctx):
        print(dt.now())


def setup(bot):
    bot.add_cog(Basic(bot))
