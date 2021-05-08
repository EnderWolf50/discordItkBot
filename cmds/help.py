import discord
from discord.ext import commands
from core import CogInit, HelpMessages

from typing import Any

class Help(CogInit):
    def _get_help_embed(self, embed_info: dict[str, Any]) -> discord.Embed:
        embed = discord.Embed(title=embed_info["title"],
                              description=embed_info["description"],
                              color=embed_info["color"])
        # Author
        embed.set_author(name=embed_info["author"] or self.bot.user.name,
                         icon_url=self.bot.user.avatar_url)
        # Footer
        embed.set_footer(text=embed_info["footer"])
        # Fields
        for command, description in embed_info["fields"]:
            embed.add_field(name=command, value=description, inline=True)
        return embed

    @commands.group(name="help", invoke_without_command=True)
    async def help(self, ctx: commands.Context) -> None:
        embed = self._get_help_embed(HelpMessages.help)
        await ctx.reply(embed=embed, delete_after=60)
        await ctx.message.delete(delay=60)

    @help.command()
    async def bzz(self, ctx: commands.Context) -> None:
        embed = self._get_help_embed(HelpMessages.bzz)
        await ctx.reply(embed=embed, delete_after=60)
        await ctx.message.delete(delay=60)

    @help.command()
    async def tdbzz(self, ctx: commands.Context) -> None:
        embed = self._get_help_embed(HelpMessages.tdbzz)
        await ctx.reply(embed=embed, delete_after=60)
        await ctx.message.delete(delay=60)

    @help.command(aliases=["ch"])
    async def choose(self, ctx: commands.Context) -> None:
        embed = self._get_help_embed(HelpMessages.choose)
        await ctx.reply(embed=embed, delete_after=60)
        await ctx.message.delete(delay=60)

    @help.command(aliases=["vote"])
    async def poll(self, ctx: commands.Context) -> None:
        embed = self._get_help_embed(HelpMessages.poll)
        await ctx.reply(embed=embed, delete_after=60)
        await ctx.message.delete(delay=60)

    @help.command()
    async def pin(self, ctx: commands.Context) -> None:
        embed = self._get_help_embed(HelpMessages.pin)
        await ctx.reply(embed=embed, delete_after=60)
        await ctx.message.delete(delay=60)

    @help.group(name="cue", aliases=["c"], invoke_without_command=True)
    async def cue(self, ctx: commands.Context) -> None:
        embed = self._get_help_embed(HelpMessages.cue)
        await ctx.reply(embed=embed, delete_after=60)
        await ctx.message.delete(delay=60)

    @cue.command(aliases=["a"])
    async def add(self, ctx: commands.Context) -> None:
        embed = self._get_help_embed(HelpMessages.cue.add)
        await ctx.reply(embed=embed, delete_after=60)
        await ctx.message.delete(delay=60)

    @cue.command(aliases=["remove", "d", "r"])
    async def delete(self, ctx: commands.Context) -> None:
        embed = self._get_help_embed(HelpMessages.cue.delete)
        await ctx.reply(embed=embed, delete_after=60)
        await ctx.message.delete(delay=60)

    @cue.command(aliases=["l"])
    async def list(self, ctx: commands.Context) -> None:
        embed = self._get_help_embed(HelpMessages.cue.list)
        await ctx.reply(embed=embed, delete_after=60)
        await ctx.message.delete(delay=60)

    @help.group(name="emoji", aliases=["e"], invoke_without_command=True)
    async def emoji(self, ctx: commands.Context) -> None:
        embed = self._get_help_embed(HelpMessages.emoji)
        await ctx.reply(embed=embed, delete_after=60)
        await ctx.message.delete(delay=60)

    @emoji.command(aliases=["r"])
    async def rank(self, ctx: commands.Context) -> None:
        embed = self._get_help_embed(HelpMessages.emoji.rank)
        await ctx.reply(embed=embed, delete_after=60)
        await ctx.message.delete(delay=60)

    @emoji.command()
    async def reset(self, ctx: commands.Context) -> None:
        embed = self._get_help_embed(HelpMessages.emoji.reset)
        await ctx.reply(embed=embed, delete_after=60)
        await ctx.message.delete(delay=60)

    @help.command()
    async def clean(self, ctx: commands.Context) -> None:
        embed = self._get_help_embed(HelpMessages.clean)
        await ctx.reply(embed=embed, delete_after=60)
        await ctx.message.delete(delay=60)

    @help.command(aliases=["is"])
    async def image_search(self, ctx: commands.Context) -> None:
        embed = self._get_help_embed(HelpMessages.image_search)
        await ctx.reply(embed=embed, delete_after=60)
        await ctx.message.delete(delay=60)


def setup(bot) -> None:
    bot.add_cog(Help(bot))
