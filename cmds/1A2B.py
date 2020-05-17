import discord
from discord.ext import commands
from core.classes import Cog_Ext

AB_G = False
ch = ""

class _1A2B(Cog_Ext):
    @commands.command()
    async def AB_G(self, ctx):
        global AB_G
        global ch
        if AB_G == False:
            AB_G = True
            ch = ctx.channel

    @commands.Cog.listener()
    async def on_message(self, msg):
        global AB_G
        global ch
        while AB_G == True:
            if msg.channel == ch:
                await msg.channel.send("輸入四個不同數字：")

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