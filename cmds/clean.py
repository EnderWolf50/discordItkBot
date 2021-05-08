import discord
from discord.ext import commands
from core import CogInit, Bot, Reactions

from asyncio import TimeoutError
from datetime import timedelta
from datetime import datetime as dt
from typing import Optional


class Clean(CogInit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.moderators = Bot.moderators

    @commands.command()
    async def clean(self,
                    ctx: commands.Context,
                    days: int = 1,
                    member: Optional[discord.Member] = None) -> None:
        # 辨認觸發指令，以及是否為管理員
        if ctx.invoked_with == "clean" or ctx.author.id not in self.moderators:
            member = self.bot.user

        # 依據是否有指定成員發送確認訊息
        confirm_msg = None
        if member is None:
            confirm_msg = await ctx.reply(f"你確定要清除 **無指定** {days} 日內的所有訊息嗎？")
        else:
            confirm_msg = await ctx.reply(
                f"你確定要清除 **{member.display_name}** {days} 日內的所有訊息嗎？")
        await confirm_msg.add_reaction(Reactions.check_mark)
        await confirm_msg.add_reaction(Reactions.cross_mark)

        def command_confirm(reaction: discord.Reaction, user: discord.User):
            if user != self.bot.user:
                if user == ctx.author and reaction.message.id == confirm_msg.id:
                    if str(reaction.emoji) == Reactions.check_mark:
                        raise ActiveCommand
                    elif str(reaction.emoji) == Reactions.cross_mark:
                        raise CancelCommand

        try:
            await self.bot.wait_for('reaction_add',
                                    timeout=10,
                                    check=command_confirm)
        # 點選確認
        except ActiveCommand:
            # 清除確認訊息
            await confirm_msg.delete()
            start_time = dt.now()

            def is_specific(m: discord.Message) -> bool:
                return member is None or m.author == member

            deleted_msg_count = len(await ctx.channel.purge(
                limit=None,
                after=dt.utcnow() - timedelta(days=days, seconds=1),
                before=ctx.message.created_at,
                oldest_first=False,
                check=is_specific))

            # 計算花費時間
            time_taken = (dt.now() - start_time).total_seconds()
            h, r = divmod(time_taken, 3600)
            m, s = divmod(r, 60)
            # 依據是否有指定成員發送結果
            if member is None:
                await ctx.reply(
                    f"已清除 {deleted_msg_count} 則 **無指定** 的訊息｜花費時長：{h:02.0f}:{m:02.0f}:{s:02.0f}",
                    delete_after=7)
            else:
                await ctx.reply(
                    f"已清除 {deleted_msg_count} 則 **{member.display_name}** 的訊息｜花費時長：{h:02.0f}:{m:02.0f}:{s:02.0f}",
                    delete_after=7)
        # 點選取消
        except CancelCommand:
            await confirm_msg.delete()
            await ctx.reply(f"指令已取消", delete_after=7)
        # 未點選
        except TimeoutError:
            await confirm_msg.delete()
            await ctx.reply(f"超過等待時間，指令已取消", delete_after=7)
        finally:
            await ctx.message.delete(delay=7)

    @commands.command()
    async def purge(self,
                    ctx: commands.Context,
                    days: int = 1,
                    member: Optional[discord.Member] = None) -> None:
        # 透過 invoke 執行
        await ctx.invoke(self.bot.get_command("clean"),
                         days=days,
                         member=member)


class ActiveCommand(Exception):
    pass


class CancelCommand(Exception):
    pass


def setup(bot):
    bot.add_cog(Clean(bot))
