import discord
from discord.ext import commands
from core.classes import Cog_Ext
import random
import datetime

AB_G = False
wait = False
Duplicate = False
Playing = False
Start_time = ""
channel = ""
Answer = ""
Number = ""
Number_Guessed = ""

class _1A2B(Cog_Ext):
    @commands.command()
    async def AB_S(self, ctx):
        global AB_G
        global channel
        global Answer
        global Start_time
        if AB_G == False:
            AB_G = True
            channel = ctx.channel
            Start_time = datetime.datetime.now() + datetime.timedelta(seconds= -5)
            Answer = random.sample('1234567890', 4)

    @commands.command()
    async def AB_E(self, ctx):
        global AB_G
        global Answer
        global Number
        global Playing
        global wait
        if AB_G == True:
            AB_G = False 
            wait = False
            Playing = False
            Number = "".join(Answer)
            def predicate(msg: discord.Message) -> bool:
                return msg.author == self.bot.get_user(710498084194484235) or (len(msg.content) == 4 and msg.content.isdigit())
            await channel.purge(after= Start_time, check= predicate)
            await channel.send(ctx.author.mention + " 結束了遊戲！")
            await channel.send("正確答案為： " + f"**{Number}**！")

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
        if msg.channel == channel:
            if AB_G == True:
                if wait == False:
                    wait = True
                    if Playing == False:
                        Playing = True
                        await channel.send("請輸入四位不同數字：")
                else:
                    if msg.content.isdigit() == True and len(msg.content) == 4:
                        Number_Guessed = list(msg.content)
                        j = 0
                        while j < 4:
                            k = 0
                            while k < 4:
                                if j == k:
                                    k += 1
                                    continue
                                if Duplicate == True:
                                    j = 4
                                    k = 4
                                else:
                                    if (Number_Guessed[j] == Number_Guessed[k]):
                                        Duplicate = True
                                k += 1
                            j += 1
                        if Duplicate == False:
                            A = 0
                            for i in range(4):
                                if (Number_Guessed[i] == Answer[i]):
                                    A += 1
                            B = 0
                            j = 0
                            while j < 4:
                                k = 0
                                while k < 4:
                                    if j == k:
                                        k += 1
                                        continue
                                    if (Number_Guessed[j] == Answer[k]):
                                        B += 1
                                    k += 1
                                j += 1
                            if A == 4:
                                AB_G = False
                                wait = False
                                Playing = False
                                def predicate(msg: discord.Message) -> bool:
                                    return msg.author == self.bot.get_user(710498084194484235) or (len(msg.content) == 4 and msg.content.isdigit())
                                await channel.purge(after= Start_time, check= predicate)
                                await channel.send(msg.author.mention + f"（{msg.content}）" + f"：**{A}A{B}B**")
                                await channel.send(f"恭喜 {msg.author.mention} 答對了！")
                            else:
                                wait = False
                                await channel.send(msg.author.mention + f"（{msg.content}）" + f"：**{A}A{B}B**")
                        else:
                            await channel.send(msg.author.mention + " 請勿輸入重複的數字！")
                            Duplicate = False


def setup(bot):
    bot.add_cog(_1A2B(bot))