import discord
from discord.ext import commands
from core.classes import Cog_Ext
import random

AB_G = False
wait = False
End = False
Duplicate = False
channel = ""
Number = ""
Number_Guessed = ""

class _1A2B(Cog_Ext):
    @commands.command()
    async def AB_G(self, ctx):
        global AB_G
        global channel
        global Number
        if AB_G == False:
            AB_G = True
            channel = ctx.channel
            Number = random.sample('1234567890', 4)
            
    @commands.command()
    async def g(self, ctx, num):
        global AB_G
        global Number_Guessed
        global channel
        if AB_G == True:
            Number_Guessed = list(num)
            await ctx.send(Number_Guessed)

    @commands.Cog.listener()
    async def on_message(self, msg):
        global AB_G
        global channel
        global wait
        global Number_Guessed
        global Number
        global End
        global Duplicate
        if msg.channel == channel:
            if AB_G == True:
                if wait == False:
                    wait = True
                    await channel.send("請輸入四位不同數字：")
                else:
                    if msg.content.isdigit() == True and len(msg.content) ==4:
                        Number_Guessed = list(msg.content)
                        j = 0
                        while j < 4:
                            k = 0
                            while k < 4:
                                if j == k:
                                    k += 1
                                    continue
                                if Duplicate == True:
                                    await channel.send("No!")
                                else:
                                    if (Number_Guessed[j] == Number_Guessed[k]):
                                        Duplicate = True
                                k += 1
                            j += 1
                        if Duplicate == False:
                            A = 0
                            for i in range(4):
                                if (Number_Guessed[i] == Number[i]):
                                    A += 1
                            B = 0
                            j = 0
                            while j < 4:
                                k = 0
                                while k < 4:
                                    if j == k:
                                        k += 1
                                        continue
                                    if (Number_Guessed[j] == Number[k]):
                                        B += 1
                                    k += 1
                                j += 1
                            if A == 4:
                                AB_G = False
                                wait = False
                                await channel.send(msg.author.mention + f"（{msg.content}）" + f"：**{A}A{B}B**")
                                await channel.send(f"恭喜 {msg.author.mention} 答對了！")
                            else:
                                wait = False
                                await channel.send(msg.author.mention + f"（{msg.content}）" + f"：**{A}A{B}B**")


def setup(bot):
    bot.add_cog(_1A2B(bot))

"""
import random
x=random.sample('1234567890',4)
print (x)
play=True
while play:
    y=input("輸入4個不同數字:")
    print (y)
    z = list(y)
    print (z)
    a=0
    for i in range(4):
        if(x[i]==z[i]):
            a=a+1
    b=0
    j=0
    while j < 4:
        k=0
        while k < 4:
            if j==k :
                k=k+1
                continue
            if(x[j]==z[k]):
                b=b+1
            k=k+1
        j=j+1
     
    print(a,"A", b, "B")
    if a == 4:
        play = False
"""