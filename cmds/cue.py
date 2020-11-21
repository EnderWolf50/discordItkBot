import discord
from discord.ext import commands
from core.classes import Cog_Ext

import random

words_list = ['加母鴨', '拉大筋天', '路滷味', '大艙酷', '麻爛郭', '拋山怪', '我錯了 請綁我(?']


class Cue(Cog_Ext):
    @commands.command()
    async def Cue(self, ctx):
        word = random.choice(words_list)
        await ctx.send(
            f'<@!429992095374114826> 語錄 {words_list.index(word)+1} - {word}')

    @commands.command()
    async def Cue_add(self, ctx, *, word):
        words_list.append(word)
        await self.bot.get_channel(725295821456801845).send(words_list)

    @commands.command()
    async def Cue_del(self, ctx, num: int):
        word_temp = words_list[num - 1]
        del words_list[num - 1]
        await ctx.send(f'已成功刪除語錄 {num} - {word_temp}')
        await self.bot.get_channel(725295821456801845).send(words_list)

    @commands.command()
    async def Cue_list(self, ctx):
        msg_temp = ''
        for i in range(len(words_list)):
            msg_temp += f'{i+1}. {words_list[i]}\n'
        await ctx.send(msg_temp)


def setup(bot):
    bot.add_cog(Cue(bot))