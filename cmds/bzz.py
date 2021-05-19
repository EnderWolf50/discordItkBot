import random
from datetime import datetime as dt

from core import CogInit, Fun, Mongo
from discord.ext import commands


class Bzz(CogInit):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.mongo = Mongo("discord_669934356172636199", "tdbzz_record")

        self.bzz_options = Fun.bzz.options
        self.tdbzz_options = Fun.tdbzz.options

    @commands.command()
    async def bzz(self, ctx: commands.Context) -> None:
        await ctx.reply(random.choice(self.bzz_options), delete_after=15)
        await ctx.message.delete(delay=15)

    @commands.command()
    async def tdbzz(self, ctx: commands.Context) -> None:
        now = dt.now()
        record = self.mongo.find({"_id": now.strftime("%Y-%m-%d")})

        bzz_msg: str = ""
        if record is None or str(ctx.author.id) not in record:
            bzz_msg = random.choice(self.tdbzz_options)
            self.mongo.update(
                {"_id": now.strftime("%Y-%m-%d")},
                {
                    "$set": {
                        f"{ctx.author.id}": bzz_msg,
                    }
                },
            )
        else:
            bzz_msg = record[f"{ctx.author.id}"]

        await ctx.reply(
            ctx.author.mention + f" 你今日（{now.strftime('%m / %d')}）的運勢為：" + bzz_msg,
            delete_after=15,
        )
        await ctx.message.delete(delay=15)


def setup(bot) -> None:
    bot.add_cog(Bzz(bot))
