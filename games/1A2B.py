import discord
from discord.ext import commands
from core.classes import Cog_Ext
from typing import List

import random
import datetime
import asyncio
import json

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
messages_during_the_game: List[discord.Message] = []


class _1A2B(Cog_Ext):
    @commands.command(aliases=['ab_s'])
    async def ab_start(self, ctx, num: int = 4):
        global AB_G
        global channel
        global Answer
        global Start_time
        global Amount
        await ctx.message.delete(delay=5)
        if AB_G == False:
            if 0 < num <= 10:
                AB_G = True
                channel = ctx.channel
                Amount = num
                Start_time = ctx.message
                Answer = random.sample('1234567890', Amount)

    @commands.command(aliases=['ab_e'])
    async def ab_end(self, ctx):
        global AB_G
        global Answer
        global Number
        global Playing
        global wait
        await ctx.message.delete(delay=5)
        if AB_G == True:
            AB_G = False
            wait = False
            Playing = False
            Number = "".join(Answer)
            End_Time = datetime.datetime.now() + datetime.timedelta(seconds=-5)

            def predicate(msg: discord.Message) -> bool:
                return msg.author == self.bot.get_user(710498084194484235) or (
                    len(msg.content) == Amount and msg.content.isdigit())

            await asyncio.sleep(0.5)
            await channel.send(ctx.author.mention + " 結束了遊戲！")
            await channel.send("正確答案為： " + f"**{Number}**！")
            await asyncio.sleep(5)
            await channel.purge(after=Start_time,
                                before=End_Time,
                                check=predicate)

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
                        messages_during_the_game.append(
                            await channel.send(f"請輸入 {Amount} 位不同數字："))
                else:
                    if msg.content.isdigit() == True and len(
                            msg.content) == Amount:
                        Number_Guessed = list(msg.content)
                        A = 0
                        B = 0
                        for i in range(Amount):
                            for j in range(Amount):
                                if i != j:
                                    if Number_Guessed[i] == Number_Guessed[j]:
                                        Duplicate = True
                                        break
                                    elif Number_Guessed[i] == Answer[j]:
                                        B += 1
                                else:
                                    if Number_Guessed[i] == Answer[j]:
                                        A += 1
                            if Duplicate == True:
                                break
                        if Duplicate == False:
                            if A == Amount:
                                AB_G = False
                                wait = False
                                Playing = False
                                End_Time = datetime.datetime.now(
                                ) + datetime.timedelta(seconds=5)

                                def predicate(msg: discord.Message) -> bool:
                                    return msg in messages_during_the_game

                                await asyncio.sleep(0.5)
                                await channel.send(msg.author.mention +
                                                   f"（{msg.content}）" +
                                                   f"：**{A}A{B}B**")
                                await channel.send(
                                    f"恭喜 {msg.author.mention} 答對了！")
                                await asyncio.sleep(5)
                                await channel.purge(limit=0,
                                                    after=Start_time,
                                                    check=predicate)
                            else:
                                wait = False
                                messages_during_the_game.append(
                                    await channel.send(msg.author.mention +
                                                       f"（{msg.content}）" +
                                                       f"：**{A}A{B}B**"))
                        else:
                            messages_during_the_game.append(
                                await channel.send(msg.author.mention +
                                                   " 請勿輸入重複的數字！"))
                            Duplicate = False
                        if msg.guild:
                            messages_during_the_game.append(msg)


def setup(bot):
    bot.add_cog(_1A2B(bot))
