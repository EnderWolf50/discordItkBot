import logging

from bot import ItkBot
from bot.configs import Emojis
from bot.core import CogInit
from bot.utils import reply_then_delete
from discord.ext import commands
from discord.ext.commands import errors

logger = logging.getLogger(__name__)


class Basic(CogInit):
    async def _ext_act(self, action: str, path: str) -> str:
        try:
            if action == "reload" or action == "rl":
                self.bot.reload_extension(path)
                return f"**{path}** has been reloaded!"
            elif action == "unload" or action == "ul":
                self.bot.unload_extension(path)
                return f"**{path}** has been unloaded!"
            elif action == "load" or action == "l":
                self.bot.load_extension(path)
                return f"**{path}** has been loaded!"
            else:
                raise NotAnAction(
                    f"Got an unexpected action {action}.", name=path, action=action
                )
        except errors.ExtensionAlreadyLoaded as e:
            logger.error(e)
            return f"**{path}** is already loaded."
        except errors.ExtensionFailed as e:
            logger.error(e)
            return f"An error occurred when trying to {action} **{path}**."
        except errors.ExtensionNotFound as e:
            logger.error(e)
            return f"There has no extension named **{path}**"
        except errors.ExtensionNotLoaded as e:
            logger.error(e)
            return f"**{path}** is not loaded yet."
        except NotAnAction as e:
            logger.error(e)
            return f"**{action}** is not a valid action."

    @commands.command(aliases=["ext"])
    async def extension(self, ctx: commands.Context, action: str, *input_path) -> None:
        if not (await self.bot.is_owner(ctx.author)):
            return
        # 沒有輸入要執行動作的 extension
        if not input_path:
            await reply_then_delete(ctx, f"請輸入要執行動作的對象 {Emojis.pepe_simp}", 5)
            return

        # 僅輸入 extension
        if len(input_path) == 1:
            ext_path = self.bot.ext_path_mapping[input_path[0]]
        else:
            ext_path = f"bot.exts.{'.'.join(input_path)}"

        respond = await self._ext_act(action, ext_path)
        await reply_then_delete(ctx, respond, 5)

    @commands.command(aliases=["rl"])
    async def reload(self, ctx: commands.Context, *input_path) -> None:
        # 使舊指令可執行
        await ctx.invoke(
            self.bot.get_command("extension"), ctx.invoked_with, *input_path
        )

    @commands.command(aliases=["ul"])
    async def unload(self, ctx: commands.Context, *input_path) -> None:
        # 使舊指令可執行
        await ctx.invoke(
            self.bot.get_command("extension"), ctx.invoked_with, *input_path
        )

    @commands.command(aliases=["l"])
    async def load(self, ctx: commands.Context, *input_path) -> None:
        # 使舊指令可執行
        await ctx.invoke(
            self.bot.get_command("extension"), ctx.invoked_with, *input_path
        )

    @commands.command()
    async def ping(self, ctx: commands.Context) -> None:
        await ctx.reply(f"Pong? {round(self.bot.latency * 1000)}")


class NotAnAction(errors.ExtensionError):
    """使用者傳入意料之外的動作"""

    def __init__(self, message, *args, name, action):
        super().__init__(message=message, *args, name=name)
        self.action = action


def setup(bot: ItkBot) -> None:
    bot.add_cog(Basic(bot))
