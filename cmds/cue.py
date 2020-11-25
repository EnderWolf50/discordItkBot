import discord
from discord.ext import commands
from core.classes import Cog_Ext

import random

words_list = [
    '加母鴨', '拉大筋天', '路滷味', '大艙酷', '麻爛郭', '拋山怪', '我錯了 請綁我(?', '原來有烈恆', '鯊鯊把我下吃了',
    '雌', '捏褲', '速鞭', '後麵', '麻將乾麵', '股溝', '像練', '可惜恐嚇 可口可樂', '可惜恐嚇 可口可樂',
    'vul4n3', '韓式炸肉狗', '找一步', '溏心但', '借魚頭', '毒水', '性啥', '綠嘎理'
]

prev_msg = None
curr_msg = None

prev_list = None
curr_list = None


class Cue(Cog_Ext):
    @commands.command()
    async def Cue(self, ctx, pos: int = None):
        if pos:
            await ctx.send(
                f'<@!429992095374114826> 語錄 {pos} - {words_list[pos - 1]}')
            return
        word = random.choice(words_list)
        await ctx.send(
            f'<@!429992095374114826> 語錄 {words_list.index(word) + 1} - {word}')

    @commands.command()
    async def Cue_add(self, ctx, *, word):
        words_list.append(word)
        await ctx.send(f'已成功增加語錄 {len(words_list)} - {word}')

        global prev_msg
        if prev_msg:
            await prev_msg.delete()
            del prev_msg

        curr_msg = await self.bot.get_channel(725295821456801845).send(
            words_list)
        prev_msg = curr_msg

    @commands.command()
    async def Cue_del(self, ctx, num: int):
        word_temp = words_list[num - 1]
        del words_list[num - 1]
        await ctx.send(f'已成功刪除語錄 {num} - {word_temp}')

        global prev_msg
        if prev_msg:
            await prev_msg.delete()
            del prev_msg

        curr_msg = await self.bot.get_channel(725295821456801845).send(
            words_list)
        prev_msg = curr_msg

    @commands.command()
    async def Cue_list(self, ctx):
        msg_temp = ''
        for i in range(len(words_list)):
            msg_temp += f'{i+1}. {words_list[i]}\n'

        global prev_list
        if prev_list:
            await prev_list.delete()
            del prev_list

        curr_list = await ctx.send(msg_temp)
        prev_list = curr_list


def setup(bot):
    bot.add_cog(Cue(bot))