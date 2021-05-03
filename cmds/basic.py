import discord
from discord.ext import commands
from core import CogInit, HelpMessages


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
    async def help(self, ctx: commands.Context) -> None:
        embed_details = HelpMessages.help

        embed = discord.Embed(
            title=embed_details["title"],
            #   description=embed_details["description"],
            color=embed_details["color"])
        # Author
        embed.set_author(name=embed_details["author"] or self.bot.user.name,
                         icon_url=self.bot.user.avatar_url)
        # Footer
        embed.set_footer(text=embed_details["footer"])
        # Fields
        for command, description in embed_details["fields"]:
            embed.add_field(name=command, value=description, inline=True)
        await ctx.reply(embed=embed, delete_after=60)
        await ctx.message.delete(delay=60)

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
