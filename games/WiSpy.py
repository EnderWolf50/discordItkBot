import discord
from discord.ext import commands
from core.classes import Cog_Ext
import asyncio
import random

WIS = False
In_game = False
channel = ""
Players = []
Topics = [["咖啡", "奶茶"], ["泳褲", "內褲"]]
Spy_N = ""
Vote_msg_ID = ""
Emoji = [
            "\N{REGIONAL INDICATOR SYMBOL LETTER A}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER B}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER C}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER D}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER E}", 
            "\N{REGIONAL INDICATOR SYMBOL LETTER F}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER G}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER H}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER I}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER J}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER K}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER L}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER M}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER N}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER O}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER P}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Q}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER R}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER S}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER T}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER U}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER V}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER W}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER X}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Y}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Z}"
            ]

class WiSpy(Cog_Ext):
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)

    @commands.command()
    async def WiS(self, ctx):
        global WIS
        global channel
        global Players
        global Spy_N
        global Topics
        global In_game
        msg_P = ""
        if WIS == False:
            WIS = True
            channel = ctx.channel
            await channel.send("**誰是間諜** 遊戲已建立！")
            await channel.send("請在 60 秒內輸入 `參加` 來加入遊戲")
            #await asyncio.sleep(30)
            await channel.send("報名時間還有 30 秒，輸入 `參加` 來加入遊戲")
            #await asyncio.sleep(20)
            await channel.send("報名時間還有 10 秒，輸入 `參加` 來加入遊戲")
            await asyncio.sleep(10)
            await channel.send("遊戲報名截止！")
            for P in Players:
                msg_P = msg_P + "\n" + P.mention
            await channel.send(f"參加名單如下：{msg_P}")
            await asyncio.sleep(3)
            Spy = random.choice(Players)
            Ttt = random.choice(Topics)
            for P in Players:
                if P != Spy:
                    await P.send(Ttt[0])
                else:
                    await P.send(Ttt[1])
                await P.send(Spy)
            await channel.send("遊戲開始！")
            In_game = True
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        global WIS
        global channel
        global Players
        global In_game
        global Emoji
        global Vote_msg_ID
        if WIS == True:
            if msg.channel == channel:
                if msg.content == "參加":
                    if In_game == False:
                        if msg.author in Players:
                            await channel.send(f"{msg.author.mention} 你已經在參加名單內")
                        else:
                            Players.append(msg.author)
                            await channel.send(f"{msg.author.mention} 已加入遊戲！")
                elif msg.content == "遊戲開始！" and msg.author == self.bot.user:
                    PV = ""
                    Players_Say = []
                    for P in Players:
                        def check(msg):
                            if msg.content.startswith("說") and msg.author == P:
                                Players_Say.append(msg.content)
                                return True
                        await channel.send(f"{P.mention} 請描述你獲得的題目")
                        await self.bot.wait_for("message", check= check)
                    for i in range(len(Players)):
                        PV = PV + "\n" + Emoji[i] + " " + Players[i].mention + " " + Players_Say[i]
                    embed = discord.Embed(description= PV)
                    Vote_msg = await channel.send("誰是間諜？", embed= embed)
                    Vote_msg_ID = Vote_msg.id
                    for i in range(len(Players)):
                        await Vote_msg.add_reaction(Emoji[i])
                    await channel.send(Vote_msg_ID)
                    await asyncio.sleep(10)
                    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        global Vote_msg_ID
        Vote_Emoji = {}
        if reaction.message.id == Vote_msg_ID:
            if user != self.bot.user:
                await reaction.message.channel.send("sda")
            else:
                Vote_msg_ID["s"] = "reaction.count"
                await reaction.message.channel.send(Vote_msg_ID)

def setup(bot):
    bot.add_cog(WiSpy(bot))