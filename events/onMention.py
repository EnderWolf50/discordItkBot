import discord
from discord.ext import commands
from core.classes import Cog_Ext
from core.rwFile import rFile, wFile

import redis

subscriberList = {}

r = redis.Redis(host="redis-17540.c56.east-us.azure.cloud.redislabs.com",
                port="17540",
                password="i7KZ0dEX4TP01e8HCM20vRkvNb7U2yUr")

for key in r.keys():
	subscriberList[key.decode("utf-8")] = r.get(key).decode("utf-8").split(", ")

class On_Mention(Cog_Ext):
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.channel == self.bot.get_channel(675956755112394753) and msg.author != self.bot.user:
            if len(msg.mentions) == 1 and str(msg.mentions[0].id) in subscriberList.keys():

                subscriptionInfo = f"<@{msg.mentions[0].id}>"
                for value in subscriberList[f"{msg.mentions[0].id}"]:
                    subscriptionInfo += f"\n{value}"

                await msg.channel.send(subscriptionInfo, delete_after= 180)

def setup(bot):
    bot.add_cog(On_Mention(bot))