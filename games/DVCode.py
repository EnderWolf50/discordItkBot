import discord
from discord.ext import commands
from core.classes import Cog_Ext

import random
import datetime
import asyncio

DV_G = False
Answer = ""
channel = ""
Min = 0
Max = 0
Original_Max = 0
Start_Time = ""


class DVCode(Cog_Ext):
    @commands.command()
    async def DVCode(self, ctx, num: int):
        global DV_G
        global Answer
        global Max
        global channel
        global Start_Time
        global Original_Max
        await ctx.message.delete(delay=5)
        if num > 1:
            if DV_G == False:
                DV_G = True
                Answer = random.randrange(1, num)
                channel = ctx.channel
                Start_Time = datetime.datetime.now() + datetime.timedelta(
                    seconds=-5)
                Max = num
                Original_Max = num
                await channel.send(f"**終極密碼** 遊戲開始\n數字範圍為 **0 ~ {num}**")

    @commands.Cog.listener()
    async def on_message(self, msg):
        global DV_G
        global Answer
        global channel
        global Min, Max
        global Original_Max
        global Start_Time
        if msg.channel == channel:
            if DV_G == True:
                if msg.content.isdigit() == True and Min < int(
                        msg.content) < Max:
                    if int(msg.content) == Answer:
                        DV_G = False
                        Min = 0
                        Max = 0
                        End_Time = datetime.datetime.now()

                        def predicate(msg: discord.Message) -> bool:
                            return msg.author == self.bot.get_user(
                                710498084194484235) or (
                                    msg.content.isdigit() == True
                                    and 0 < int(msg.content) < Original_Max)

                        await asyncio.sleep(0.5)
                        await channel.send(msg.author.mention +
                                           " 猜到ㄌ\n但好像也不能幹嘛就是ㄌ")
                        await asyncio.sleep(5)
                        await channel.purge(after=Start_Time,
                                            before=End_Time,
                                            check=predicate)
                    else:
                        if int(msg.content) < Answer:
                            Min = int(msg.content)
                            await channel.send(f"現在數字範圍為 **{Min} ~ {Max}**")
                        elif int(msg.content) > Answer:
                            Max = int(msg.content)
                            await channel.send(f"現在數字範圍為 **{Min} ~ {Max}**")


def setup(bot):
    bot.add_cog(DVCode(bot))