import discord
from discord.ext import commands
from core.classes import Cog_Ext

import os, re
from saucenao_api import SauceNao

KEYS = [os.getenv('SAUCE_NAO_KEY_1'), os.getenv('SAUCE_NAO_KEY_2')]
SN1 = SauceNao(api_key=KEYS[0], numres=3)
SN2 = SauceNao(api_key=KEYS[1], numres=3)
reaction_emos = {
    "1\N{COMBINING ENCLOSING KEYCAP}": 0,
    "2\N{COMBINING ENCLOSING KEYCAP}": 1,
    "3\N{COMBINING ENCLOSING KEYCAP}": 2,
    "4\N{COMBINING ENCLOSING KEYCAP}": 3,
    "5\N{COMBINING ENCLOSING KEYCAP}": 4,
    "6\N{COMBINING ENCLOSING KEYCAP}": 5,
    "7\N{COMBINING ENCLOSING KEYCAP}": 6,
    "8\N{COMBINING ENCLOSING KEYCAP}": 7,
    "9\N{COMBINING ENCLOSING KEYCAP}": 8,
    "\N{REGIONAL INDICATOR SYMBOL LETTER A}": 9,
    "\N{REGIONAL INDICATOR SYMBOL LETTER B}": 10,
    "\N{REGIONAL INDICATOR SYMBOL LETTER C}": 11,
    "\N{REGIONAL INDICATOR SYMBOL LETTER D}": 12,
    "\N{REGIONAL INDICATOR SYMBOL LETTER E}": 13,
    "\N{REGIONAL INDICATOR SYMBOL LETTER F}": 14,
    "\N{REGIONAL INDICATOR SYMBOL LETTER G}": 15,
    "\N{REGIONAL INDICATOR SYMBOL LETTER H}": 16,
    "\N{REGIONAL INDICATOR SYMBOL LETTER I}": 17,
    "\N{REGIONAL INDICATOR SYMBOL LETTER J}": 18,
    "\N{REGIONAL INDICATOR SYMBOL LETTER K}": 19,
    "\N{REGIONAL INDICATOR SYMBOL LETTER L}": 20,
    "\N{REGIONAL INDICATOR SYMBOL LETTER M}": 21,
    "\N{REGIONAL INDICATOR SYMBOL LETTER N}": 22,
    "\N{REGIONAL INDICATOR SYMBOL LETTER O}": 23,
    "\N{REGIONAL INDICATOR SYMBOL LETTER P}": 24,
    "\N{REGIONAL INDICATOR SYMBOL LETTER Q}": 25,
    "\N{REGIONAL INDICATOR SYMBOL LETTER R}": 26,
    "\N{REGIONAL INDICATOR SYMBOL LETTER S}": 27,
    "\N{REGIONAL INDICATOR SYMBOL LETTER T}": 28,
    "\N{REGIONAL INDICATOR SYMBOL LETTER U}": 29,
    "\N{REGIONAL INDICATOR SYMBOL LETTER V}": 30,
    "\N{REGIONAL INDICATOR SYMBOL LETTER W}": 31,
    "\N{REGIONAL INDICATOR SYMBOL LETTER X}": 32,
    "\N{REGIONAL INDICATOR SYMBOL LETTER Y}": 33,
    "\N{REGIONAL INDICATOR SYMBOL LETTER Z}": 34
}

ctr = 0
res_list = {}


class ImgSearch(Cog_Ext):
    def isfloat(self, num):
        try:
            float(num)
            return True
        except:
            return False

    def embed_gen(self, i, res, remaining):
        embed = discord.Embed(title='搜尋結果', color=0xFCD992)
        embed.set_footer(
            text=f'第 {i} 張圖  |  24h 內流量: {200 - remaining} / 200',
            icon_url=
            'https://cdn.discordapp.com/avatars/710498084194484235/e91dbe68bd05239c050805cc060a34e9.webp?size=128'
        )
        if res.thumbnail:
            embed.set_thumbnail(url=res.thumbnail)
        if res.similarity:
            embed.add_field(name='相似度', value=res.similarity, inline=False)
        if res.title:
            embed.add_field(name='標題', value=res.title, inline=False)
        if res.urls:
            for url in res.urls:
                embed.add_field(name='連結', value=url + '\n', inline=False)
        if res.author:
            embed.add_field(name='作者', value=res.author, inline=False)
        if 'source' in res.raw['data'].keys():
            if res.raw['data']['source']:
                embed.add_field(name='來源',
                                value=res.raw['data']['source'],
                                inline=False)
        return embed

    def no_result_embed_gen(self, i, url, remaining):
        embed = discord.Embed(title='搜尋結果', color=0xDB4A30)
        embed.set_footer(
            text=f'第 {i} 張圖  |  24h 內流量: {200 - remaining} / 200',
            icon_url=
            'https://cdn.discordapp.com/avatars/710498084194484235/e91dbe68bd05239c050805cc060a34e9.webp?size=128'
        )
        embed.set_thumbnail(url=url)
        embed.add_field(name='沒有結果...',
                        value='藍瘦香菇 <:010:685774195904479244>',
                        inline=False)

        return embed

    @commands.command(aliases=['img_search', 'is'])
    async def Image_search(self, ctx, *args):
        global ctr
        if ctx.channel.type != discord.ChannelType.private:
            await ctx.message.delete(delay=15)
        res_embed_list = []
        lst_arg_isfloat = self.isfloat(args[-1]) if args else True
        min_similarity = float(args[-1]) if (args
                                             and lst_arg_isfloat) else 52.0
        queue = []
        if ctx.message.reference:
            ref_msg = await ctx.channel.fetch_message(
                ctx.message.reference.message_id)
            queue += [a.url for a in ref_msg.attachments] + [
                a for a in re.findall(r'https?:\/\/[^\s]*', ref_msg.content)
            ]
        if ctx.message.attachments:
            queue += [a.url for a in ctx.message.attachments]
        if (args[:-1] if lst_arg_isfloat else args):
            queue += [
                a for a in (args[:-1] if lst_arg_isfloat else args)
                if re.match(r'https?:\/\/[^\s]*', a)
            ]
        if not queue: return

        for i, q in enumerate(queue[:6], 1):
            similar_ctr = 0
            ctr += 1
            res = SN1.from_url(url=q) if ctr % 2 == 0 else SN2.from_url(url=q)
            for r in res:
                if r.similarity < min_similarity: continue
                similar_ctr += 1
                res_embed_list.append(self.embed_gen(i, r, res.long_remaining))
            if not similar_ctr:
                res_embed_list.append(
                    self.no_result_embed_gen(i, q, res.long_remaining))

        msg = await ctx.send(embed=res_embed_list[0], delete_after=300)
        res_list[msg] = [ctx.author, res_embed_list]
        for i in range(len(res_embed_list)):
            await msg.add_reaction(list(reaction_emos.keys())[i])

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot: return
        if not res_list or reaction.message not in res_list.keys(): return
        await reaction.remove(user)
        if str(reaction.emoji) not in reaction_emos.keys(): return
        if user != res_list[reaction.message][0]: return

        if reaction_emos[str(reaction.emoji)] < len(
                res_list[reaction.message][1]):
            await reaction.message.edit(embed=res_list[reaction.message][1][
                reaction_emos[str(reaction.emoji)]])

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        global res_list
        if not res_list: return
        if msg in res_list.keys():
            del res_list[msg]


def setup(bot):
    bot.add_cog(ImgSearch(bot))