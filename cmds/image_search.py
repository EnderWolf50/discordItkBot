import discord
from discord.ext import commands
from core.classes import Cog_Ext

import os
from saucenao_api import SauceNao

sn = SauceNao(api_key=os.getenv('SAUCE_NAO_KEY'), numres=3)


class ImgSearch(Cog_Ext):
    def isfloat(self, num):
        try:
            float(num)
            return True
        except:
            return False

    def embed_gen(self, data):
        embed = discord.Embed(title='搜尋結果', color=0xFCD992)
        if data.thumbnail:
            embed.set_thumbnail(url=data.thumbnail)
        if data.similarity:
            embed.add_field(name='相似度', value=data.similarity, inline=False)
        if data.title:
            embed.add_field(name='標題', value=data.title, inline=False)
        if data.urls:
            for url in data.urls:
                embed.add_field(name='連結', value=url + '\n', inline=False)
        if data.author:
            embed.add_field(name='作者', value=data.author, inline=False)
        if 'source' in data.raw['data'].keys():
            embed.add_field(name='來源',
                            value=data.raw['data']['source'],
                            inline=False)
        return embed

    # @commands.cooldown(1, 30)
    @commands.command(aliases=['img_search', 'is'])
    async def Image_search(self, ctx, *args):
        await ctx.message.delete(delay=10)
        ctr = 0
        lst_arg_isfloat = self.isfloat(args[-1]) if args else True
        min_similarity = float(args[-1]) if (args
                                             and lst_arg_isfloat) else 52.0

        for attachment in ctx.message.attachments:
            similar_enough_ctr = 0
            res = sn.from_url(url=attachment.url)
            for r in res:
                if r.similarity < min_similarity: continue
                similar_enough_ctr += 1
                await ctx.send(embed=self.embed_gen(r), delete_after=180)
            if similar_enough_ctr == 0:
                await ctx.send(content='沒有結果 <:021:685800580958126081>',
                               delete_after=7)
            ctr += 1
            if ctr == 6: return
        for arg in args[:-1] if lst_arg_isfloat else args:
            similar_enough_ctr = 0
            res = sn.from_url(url=arg)
            for r in res:
                if r.similarity < min_similarity: continue
                await ctx.send(embed=self.embed_gen(r), delete_after=180)
            if similar_enough_ctr == 0:
                await ctx.send(content='沒有結果 <:021:685800580958126081>',
                               delete_after=7)
            ctr += 1
            if ctr == 6: return


def setup(bot):
    bot.add_cog(ImgSearch(bot))