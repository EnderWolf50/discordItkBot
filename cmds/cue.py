import discord
from discord.ext import commands
from core.classes import Cog_Ext

import random

words_list = ['加母鴨', '拉大筋天']


class Cue(Cog_Ext):
    @commands.command()
    async def Cue(self, ctx):
        word = random.choice(words_list)
        await ctx.send(
            f'<@!429992095374114826> 語錄 {words_list.index(word)+1}: {word}')

    @commands.command()
    async def Cue_add(self, ctx, word):
        words_list.append(word)
        await self.bot.get_channel(725295821456801845).send(words_list)


def setup(bot):
    bot.add_cog(Cue(bot))