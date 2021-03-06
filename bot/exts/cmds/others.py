import discord
from bot import ItkBot
from bot.core import CogInit
from discord.ext import commands


class Others(CogInit):
    @commands.command()
    async def cls(self, ctx: commands.Context) -> None:
        # 只能在私訊內執行
        if ctx.channel.type != discord.ChannelType.private:
            return

        # 私訊頻道無法大量清除
        msg_list = await ctx.channel.history(limit=None).flatten()
        for msg in msg_list:
            # 僅能刪除自己訊息
            if msg.author == self.bot.user:
                await msg.delete()


def setup(bot: ItkBot) -> None:
    bot.add_cog(Others(bot))
