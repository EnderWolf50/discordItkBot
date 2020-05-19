import discord
from discord.ext import commands
from core.classes import Cog_Ext
import time

WIS = False
channel = ""

class WiSpy(Cog_Ext):
    @commands.command()
    async def WiS(self, ctx):
        global WIS
        global channel
        if WIS == False:
            WIS = True
            channel = ctx.channel
            await ctx.send("**誰是間諜** 遊戲已建立！")
            await ctx.send("請在 60 秒內輸入**__「加入」__**來加入遊戲！")
    
    @commands.Cog.listener()
    async def on_message(self, ctx):
        pass

def setup(bot):
    bot.add_cog(WiSpy(bot))