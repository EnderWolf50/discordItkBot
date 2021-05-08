import discord
from discord.ext import commands
from core import CogInit, HelpMessages

from typing import Any


class Basic(CogInit):
    @commands.group(name="extension", aliases=["ext"])
    async def extension(self, ctx: commands.Context) -> None:
        # 僅用作 Group
        pass

    @extension.command(aliases=['l'])
    async def load(self, ctx: commands.Context, *input_path) -> None:
        if not (await self.bot.is_owner(ctx.author)): return

        ext_path = ".".join(input_path)
        self.bot.load_extension(ext_path)

        await ctx.reply(f"**{ext_path}** has been loaded!", delete_after=5)
        await ctx.message.delete(delay=5)

    @extension.command(aliases=['u'])
    async def unload(self, ctx: commands.Context, *input_path) -> None:
        if not (await self.bot.is_owner(ctx.author)): return

        ext_path = ".".join(input_path)
        self.bot.unload_extension(ext_path)

        await ctx.reply(f"**{ext_path}** has been unloaded!", delete_after=5)
        await ctx.message.delete(delay=5)

    @extension.command(aliases=['r'])
    async def reload(self, ctx: commands.Context, *input_path) -> None:
        if not (await self.bot.is_owner(ctx.author)): return

        ext_path = ".".join(input_path)
        self.bot.reload_extension(ext_path)

        await ctx.reply(f"**{ext_path}** has been reloaded!", delete_after=5)
        await ctx.message.delete(delay=5)

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.reply(f"Pong? {round(self.bot.latency * 1000)}")

    @commands.command(aliases=["load"])
    async def ext_load(self, ctx: commands.Context, *input_path) -> None:
        # 使舊指令可執行
        await ctx.invoke(self.bot.get_command("extension load"), *input_path)

    @commands.command(aliases=["unload"])
    async def ext_unload(self, ctx: commands.Context, *input_path) -> None:
        # 使舊指令可執行
        await ctx.invoke(self.bot.get_command("extension unload"), *input_path)

    @commands.command(aliases=["reload"])
    async def ext_reload(self, ctx: commands.Context, *input_path) -> None:
        # 使舊指令可執行
        await ctx.invoke(self.bot.get_command("extension reload"), *input_path)


def setup(bot) -> None:
    bot.add_cog(Basic(bot))
