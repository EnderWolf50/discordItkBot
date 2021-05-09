import logging

from core import CogInit, Emojis
from discord.ext import commands
from discord.ext.commands import errors
from sentry_sdk import push_scope

logger = logging.getLogger(__name__)


class ErrorHandlers(CogInit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, e: errors.CommandError
    ) -> None:
        if hasattr(e, "handled"):
            return

        if isinstance(e, errors.CommandInvokeError):
            await self.command_invoke_error_handler(ctx, e)
        elif isinstance(e, errors.UserInputError):
            await self.user_input_error_handler(ctx, e)
        elif isinstance(e, errors.CheckFailure):
            await self.check_failure_handler(ctx, e)
        elif isinstance(e, errors.DisabledCommand):
            await ctx.message.delete(delay=13)
            await ctx.reply("該指令無法直接使用或被禁用", delete_after=13)
        elif isinstance(e, errors.CommandOnCooldown):
            await ctx.message.delete(delay=13)
            await ctx.reply(
                f"該指令還在冷卻，請待訊息消失後重試 ( {e.retry_after:.1f}s )。",
                delete_after=e.retry_after,
            )
            return
        elif isinstance(e, errors.CommandNotFound):
            return  # Ignore
        else:
            await self._unexpected_error_handler(ctx, e)
            return

        logger.debug(
            f"Command {ctx.command} invoked by {ctx.author} ({ctx.author.id}) | "
            f"{e.__class__.__name__}: {e}",
            exc_info=e,
        )

    async def command_invoke_error_handler(
        self, ctx: commands.Context, e: errors.CommandInvokeError
    ):
        await ctx.message.delete(delay=13)
        await ctx.reply(f"指令執行時發生錯誤，看來又要除蟲了 {Emojis.pepe_coffee}", delete_after=13)

    async def user_input_error_handler(
        self, ctx: commands.Context, e: errors.UserInputError
    ) -> None:
        if isinstance(e, errors.BadArgument):
            await self.bad_argument_handler(ctx, e)
        elif isinstance(e, errors.MissingRequiredArgument):
            await ctx.message.delete(delay=13)
            await ctx.reply(f"你好像少打了一些東西 {Emojis.pepe_hmm}？", delete_after=13)
        elif isinstance(e, errors.ArgumentParsingError):
            await ctx.message.delete(delay=13)
            await ctx.reply(f"你的括號有點錯誤喔 {Emojis.pepe_coin}", delete_after=13)
        elif isinstance(e, errors.BadUnionArgument):
            await ctx.message.delete(delay=13)
            await ctx.reply(f"無法轉換輸入的參數 {Emojis.bongo_pepe}", delete_after=13)
        elif isinstance(e, errors.TooManyArguments):
            await ctx.message.delete(delay=13)
            await ctx.reply(
                f"看到這個訊息代表我腦抽關了某個功能 {Emojis.pepe_facepalm}", delete_after=13
            )
            return
        await ctx.send(f"指令用法：`{ctx.command.help}`", delete_after=10)

    @staticmethod
    async def bad_argument_handler(
        ctx: commands.Context, e: errors.BadUnionArgument
    ) -> None:
        if isinstance(e, errors.MessageNotFound):
            await ctx.message.delete(delay=13)
            await ctx.reply(
                f"我找不到 {e.argument} 所指定的訊息 {Emojis.pepe_sad}", delete_after=13
            )
        elif isinstance(e, errors.ChannelNotFound):
            await ctx.message.delete(delay=13)
            await ctx.reply(
                f"我找不到 {e.argument} 所指定的頻道 {Emojis.pepe_sad}", delete_after=13
            )
        elif isinstance(e, errors.RoleNotFound):
            await ctx.message.delete(delay=13)
            await ctx.reply(
                f"我找不到 {e.argument} 所指定的身分組 {Emojis.pepe_sad}", delete_after=13
            )
        elif isinstance(e, (errors.UserNotFound, errors.MemberNotFound)):
            await ctx.message.delete(delay=13)
            await ctx.reply(
                f"我找不到 {e.argument} 所指定的使用者 {Emojis.pepe_sad}", delete_after=13
            )
        elif isinstance(e, errors.EmojiNotFound):
            await ctx.message.delete(delay=13)
            await ctx.reply(
                f"我找不到 {e.argument} 所指定的表情符號 {Emojis.pepe_sad}", delete_after=13
            )
        elif isinstance(e, errors.PartialEmojiConversionFailure):
            await ctx.message.delete(delay=13)
            await ctx.reply(
                f"我無法將 {e.argument} 轉成對應的表情符號 {Emojis.pepe_sad}", delete_after=13
            )
        elif isinstance(e, errors.BadBoolArgument):
            await ctx.message.delete(delay=13)
            await ctx.reply(
                f"我不確定 {e.argument} 所代表的布林值 {Emojis.pepe_sad}", delete_after=13
            )
        elif isinstance(e, errors.BadInviteArgument):
            await ctx.message.delete(delay=13)
            await ctx.reply(f"你給予的邀請連結好像過期了欸 {Emojis.pepe_sus}", delete_after=13)
        elif isinstance(e, (errors.BadColourArgument, errors.BadColorArgument)):
            await ctx.message.delete(delay=13)
            await ctx.reply(
                f"我無法將 {e.argument} 轉成對應的顏色，請將其改為 `#<HEX>` 格式 {Emojis.pepe_simp}",
                delete_after=13,
            )
        elif isinstance(e, errors.ChannelNotReadable):
            await ctx.message.delete(delay=13)
            await ctx.reply(f"窩沒有讀取這個頻道的權限 {Emojis.pepe_hands}", delete_after=13)
        else:
            await ctx.message.delete(delay=13)
            await ctx.reply(f"不知道你打錯了什麼，我想你可以重試看看 {Emojis.pepe_hmm}", delete_after=13)

    @staticmethod
    async def check_failure_handler(
        ctx: commands.Context, e: errors.CheckFailure
    ) -> None:
        bot_missing_errors = (
            errors.BotMissingAnyRole,
            errors.BotMissingPermissions,
            errors.BotMissingRole,
        )

        user_missing_errors = (
            errors.MissingAnyRole,
            errors.MissingPermissions,
            errors.MissingRole,
        )
        if isinstance(e, user_missing_errors):
            await ctx.message.delete(delay=13)
            await ctx.reply(f"你沒有足夠的權限執行指令 {Emojis.pepe_nopes}", delete_after=13)
        elif isinstance(e, bot_missing_errors):
            await ctx.message.delete(delay=13)
            await ctx.reply(f"我沒有足夠的權限執行指令 {Emojis.pepe_depressed}", delete_after=13)
        elif isinstance(e, errors.PrivateMessageOnly):
            await ctx.message.delete(delay=13)
            await ctx.reply(
                f"這個指令只能在私人訊息中使用 {Emojis.rainbow_pepe_angry}", delete_after=13
            )
        elif isinstance(e, errors.NoPrivateMessage):
            await ctx.message.delete(delay=13)
            await ctx.reply(
                f"這個指令無法在私人訊息中使用 {Emojis.rainbow_pepe_angry}", delete_after=13
            )
        elif isinstance(e, errors.NSFWChannelRequired):
            await ctx.message.delete(delay=13)
            await ctx.reply(f"請不要在這裡開車 {Emojis.pepe_monkaSTEER}", delete_after=13)
        elif isinstance(e, errors.NotOwner):
            await ctx.message.delete(delay=13)
            await ctx.reply(f"這個指令只有作者才可以用喔 {Emojis.pepe_crown_flip}", delete_after=13)
        elif isinstance(e, errors.CheckAnyFailure):
            await ctx.message.delete(delay=13)
            await ctx.reply(
                f"以下檢查項目未通過 `{'`, `'.join({e.__class__.__name__ for e in e.errors})}` "
                "{Emojis.pepe_hmm}",
                delete_after=13,
            )

    @staticmethod
    async def _unexpected_error_handler(
        ctx: commands.Context, e: errors.CommandError
    ) -> None:
        with push_scope() as scope:
            scope.user = {"id": ctx.author.id, "username": str(ctx.author)}

            scope.set_tag("command", ctx.command.qualified_name)
            scope.set_tag("message_id", ctx.message.id)
            scope.set_tag("channel_id", ctx.channel.id)

            scope.set_extra("message_content", ctx.message.content)

            if ctx.guild is not None:
                scope.set_extra(
                    "jump_to",
                    "https://discordapp.com/channels/"
                    f"{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id}",
                )

            logger.error(
                "Error executing command invoked by "
                f"{ctx.message.author}: {ctx.message.content}",
                exc_info=e,
            )


def setup(bot) -> None:
    bot.add_cog(ErrorHandlers(bot))
