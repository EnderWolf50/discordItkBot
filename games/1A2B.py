import discord
from discord.ext import commands
from core.classes import Cog_Ext
import random
import datetime
import asyncio

AB_G = False
wait = False
Duplicate = False
Playing = False
Amount = 0
Start_time = ""
channel = ""
Answer = ""
Number = ""
Number_Guessed = ""

class _1A2B(Cog_Ext):
    @commands.command()
    async def AB_S(self, ctx, num: int= 4):
        global AB_G
        global channel
        global Answer
        global Start_time
        global Amount
        await ctx.message.delete(delay= 5)
        if AB_G == False:
            if 0 < num <= 10:
                AB_G = True
                channel = ctx.channel
                Amount = num
                Start_time = datetime.datetime.now() + datetime.timedelta(seconds= -5)
                Answer = random.sample('1234567890', Amount)

    @commands.command()
    async def AB_E(self, ctx):
        global AB_G
        global Answer
        global Number
        global Playing
        global wait
        await ctx.message.delete(delay= 5)
        if AB_G == True:
            AB_G = False 
            wait = False
            Playing = False
            Number = "".join(Answer)
            End_Time = datetime.datetime.now()
            def predicate(msg: discord.Message) -> bool:
                return msg.author == self.bot.get_user(710498084194484235) or (len(msg.content) == Amount and msg.content.isdigit())
            await asyncio.sleep(0.5)
            await channel.send(ctx.author.mention + " 結束了遊戲！")
            await channel.send("正確答案為： " + f"**{Number}**！")
            await asyncio.sleep(5)
            await channel.purge(after= Start_time, before= End_Time, check= predicate)

    @commands.Cog.listener()
    async def on_message(self, msg):
        global AB_G
        global channel
        global wait
        global Number_Guessed
        global Answer
        global Duplicate
        global Playing
        global Start_time
        global Amount
        if msg.channel == channel:
            if AB_G == True:
                if wait == False:
                    wait = True
                    if Playing == False:
                        Playing = True
                        await channel.send(f"請輸入 {Amount} 位不同數字：")
                else:
                    if msg.content.isdigit() == True and len(msg.content) == Amount:
                        Number_Guessed = list(msg.content)
                        j = 0
                        while j < Amount:
                            k = 0
                            while k < Amount:
                                if j == k:
                                    k += 1
                                    continue
                                if Duplicate == True:
                                    j = Amount
                                    k = Amount
                                else:
                                    if (Number_Guessed[j] == Number_Guessed[k]):
                                        Duplicate = True
                                k += 1
                            j += 1
                        if Duplicate == False:
                            A = 0
                            for i in range(Amount):
                                if (Number_Guessed[i] == Answer[i]):
                                    A += 1
                            B = 0
                            j = 0
                            while j < Amount:
                                k = 0
                                while k < Amount:
                                    if j == k:
                                        k += 1
                                        continue
                                    if (Number_Guessed[j] == Answer[k]):
                                        B += 1
                                    k += 1
                                j += 1
                            if A == Amount:
                                AB_G = False
                                wait = False
                                Playing = False
                                End_Time = datetime.datetime.now()
                                def predicate(msg: discord.Message) -> bool:
                                    return msg.author == self.bot.get_user(710498084194484235) or (len(msg.content) == Amount and msg.content.isdigit())
                                await asyncio.sleep(0.5)
                                await channel.send(msg.author.mention + f"（{msg.content}）" + f"：**{A}A{B}B**")
                                await channel.send(f"恭喜 {msg.author.mention} 答對了！")
                                await asyncio.sleep(5)
                                await channel.purge(after= Start_time, before= End_Time, check= predicate)
                            else:
                                wait = False
                                await channel.send(msg.author.mention + f"（{msg.content}）" + f"：**{A}A{B}B**")
                        else:
                            await channel.send(msg.author.mention + " 請勿輸入重複的數字！")
                            Duplicate = False


def setup(bot):
    bot.add_cog(_1A2B(bot))