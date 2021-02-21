import discord
from discord.ext import commands
from core.classes import Cog_Ext
from core.rwFile import get_setting

import datetime

Owner = get_setting("Owner")
Traveler = get_setting("Traveler")
Bot = get_setting("Bot")

administrators = [
    get_setting("Owner"),
    get_setting("Traveler"),
    get_setting("Juxta")
]


# TODO: 改寫判斷
# TODO: 嘗試以訊息 ID 刪除
class Clean(Cog_Ext):
    @commands.command()
    async def clean(self, ctx, number: int = 1, ID: discord.Member = None):
        await ctx.message.delete()
        if ctx.channel == self.bot.get_channel(
                675956755112394753) and ctx.author.id not in administrators:
            return
        if ID == None:
            ID = self.bot.user

        if ID.bot == False:
            return

        def predicate(msg: discord.Message) -> bool:
            return msg.author == ID

        def Command_check(reaction, user):
            if user != self.bot.user and user == ctx.author and reaction.message.id == Check_msg.id:
                if str(reaction.emoji) == "\N{WHITE HEAVY CHECK MARK}":
                    raise ActiveCommand
                else:
                    raise CancelCommand

        Check_msg = await ctx.send(
            f"{ctx.author.mention} 你確定要清除 `{ID.name}` `{number}` 日內的所有訊息嗎？")
        await Check_msg.add_reaction("\N{WHITE HEAVY CHECK MARK}")
        await Check_msg.add_reaction("\N{NEGATIVE SQUARED CROSS MARK}")

        try:
            await self.bot.wait_for('reaction_add',
                                    timeout=7.5,
                                    check=Command_check)
        except ActiveCommand:
            await Check_msg.delete()
            Start_Time = datetime.datetime.now()
            deleted_msg_count = len(
                await ctx.channel.purge(limit=None,
                                        after=datetime.datetime.now() -
                                        datetime.timedelta(days=number),
                                        check=predicate))
            End_Time = datetime.datetime.now()
            During = (End_Time - Start_Time).seconds
            await ctx.send(
                f"> 已清除 {deleted_msg_count} 則 {ID.name} 的訊息（{During}s）",
                delete_after=5)
        except CancelCommand:
            await Check_msg.delete()
            await ctx.send(f"{ctx.author.mention} 指令已取消", delete_after=5)
        except:
            await Check_msg.delete()
            await ctx.send(f"{ctx.author.mention} 超過等待時間，指令已取消",
                           delete_after=5)

    @commands.command()
    async def purge(self, ctx, number: int, ID: discord.Member = None):
        if ctx.author == self.bot.get_user(
                Owner) or ctx.author == self.bot.get_user(Traveler):
            await ctx.message.delete()

            def predicate(msg: discord.Message) -> bool:
                return ID == None or msg.author == ID

            def Command_check(reaction, user):
                if user != self.bot.user and user == ctx.author and reaction.message.id == Check_msg.id:
                    if str(reaction.emoji) == "\N{WHITE HEAVY CHECK MARK}":
                        raise ActiveCommand
                    else:
                        raise CancelCommand

            if ID == None:
                Check_msg = await ctx.send(
                    f"{ctx.author.mention} 你確定要清除 `無指定` 的 `{number}` 則訊息嗎？")
                await Check_msg.add_reaction("\N{WHITE HEAVY CHECK MARK}")
                await Check_msg.add_reaction("\N{NEGATIVE SQUARED CROSS MARK}")

                try:
                    await self.bot.wait_for('reaction_add',
                                            timeout=7.5,
                                            check=Command_check)
                except ActiveCommand:
                    await Check_msg.delete()
                    Start_Time = datetime.datetime.now()
                    deleted_msg_count = len(await
                                            ctx.channel.purge(limit=number,
                                                              check=predicate))
                    End_Time = datetime.datetime.now()
                    During = (End_Time - Start_Time).seconds
                    await ctx.send(f"> 已清除 {deleted_msg_count} 則訊息（{During}s）",
                                   delete_after=5)
                except CancelCommand:
                    await Check_msg.delete()
                    await ctx.send(f"{ctx.author.mention} 指令已取消",
                                   delete_after=5)
                except:
                    await Check_msg.delete()
                    await ctx.send(f"{ctx.author.mention} 超過等待時間，指令已取消",
                                   delete_after=5)

            else:
                DC_Member = str(ID)[:-5]
                Check_msg = await ctx.send(
                    f"{ctx.author.mention} 你確定要刪除近期 `{number}` 則訊息中 `{DC_Member}` 的所有訊息嗎？"
                )
                await Check_msg.add_reaction("\N{WHITE HEAVY CHECK MARK}")
                await Check_msg.add_reaction("\N{NEGATIVE SQUARED CROSS MARK}")

                try:
                    await self.bot.wait_for('reaction_add',
                                            timeout=7.5,
                                            check=Command_check)
                except ActiveCommand:
                    await Check_msg.delete()
                    Start_Time = datetime.datetime.now()
                    deleted_msg_count = len(await
                                            ctx.channel.purge(limit=number,
                                                              check=predicate))
                    End_Time = datetime.datetime.now()
                    During = (End_Time - Start_Time).seconds
                    await ctx.send(
                        f"> 已清除 {deleted_msg_count} 則 {DC_Member} 的訊息（{During}s）",
                        delete_after=5)
                except CancelCommand:
                    await Check_msg.delete()
                    await ctx.send(f"{ctx.author.mention} 指令已取消",
                                   delete_after=5)
                except:
                    await Check_msg.delete()
                    await ctx.send(f"{ctx.author.mention} 超過等待時間，指令已取消",
                                   delete_after=5)


class ActiveCommand(Exception):
    pass


class CancelCommand(Exception):
    pass


def setup(bot):
    bot.add_cog(Clean(bot))
