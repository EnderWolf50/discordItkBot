import discord
from discord.ext import commands
from core.classes import Cog_Ext
import random

class Roll(Cog_Ext):
    @commands.command()
    async def roll(self, ctx, num: int, *,arg= "{}"):
        if num <= 0:
            await ctx.send("ㄐㄐ")
            await ctx.send("雞雞")
            await ctx.send("尻尻")    
        else:
            if "{}" in arg:
                msg = arg.replace("{}", f"{random.randrange(1, num + 1)}", 1)
                await ctx.send(msg)
            elif "%" in arg:
                msg = arg.replace("%", f"{random.randrange(1, num + 1)}", 1)
                await ctx.send(msg)
            else:
                await ctx.send(arg + " {}".format(random.randrange(1, num + 1)))
        # else:
        #     with open("others.json", "r", encoding= "utf-8") as jothers:
        #         other = json.load(jothers)
        #     await ctx.send(other["Roll Message"].format(random.randrange(1, num + 1)))

    # @commands.command()
    # async def setrm(self, ctx, *,arg):
    #     if ctx.author == self.bot.get_user(590430031281651722) or ctx.author == self.bot.get_user(523755296242270210):
    #         with open("others.json", "r", encoding= "utf-8") as jothers:
    #             other = json.load(jothers)

    #             other["Roll Message"] = arg

    #         with open("others.json", "w", encoding= "utf-8") as jothers:
    #             json.dump(other, jothers, indent= 4)

    #         await ctx.send("訊息已設定為 __" + other["Roll Message"] + "__")

def setup(bot):
    bot.add_cog(Roll(bot))