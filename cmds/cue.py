import discord
from discord.ext import commands
from core import CogInit, Mongo

import random, math
from datetime import datetime, timedelta

cue_embed = []


class Cue(CogInit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._db = 'discord_669934356172636199'
        self._coll = 'cue_list'

    @commands.command(aliases=['c'])
    async def cue(self, ctx, member: discord.Member = None, pos: int = None):
        member_cue = None
        if member:
            member_cue = Mongo.find(self._db, self._coll, {'_id': member.id})
        if member_cue:
            member_cue_list = member_cue['list']
            if pos:
                await ctx.send(
                    f'{member.display_name} 語錄 {pos} - {member_cue_list[pos - 1]}'
                )
                await ctx.message.delete()
                return
            word = random.choice(member_cue_list)
            await ctx.send(
                f'{member.display_name} 語錄 {member_cue_list.index(word) + 1} - {word}'
            )
            await ctx.message.delete()
            return
        cue_list = {
            doc['_id']: doc['list']
            for doc in Mongo.find(self._db, self._coll)
        }
        random_cue_id = random.choice(list(cue_list.keys()))
        random_member = self.bot.get_user(random_cue_id)
        random_pos = random.randint(0, len(cue_list[random_cue_id]) - 1)
        random_word = cue_list[random_cue_id][random_pos]
        await ctx.send(
            f'{random_member.display_name} 語錄 {random_pos + 1} - {random_word}',
        )
        await ctx.message.delete()
        return

    @commands.command(aliases=['c_a', 'ca'])
    async def cue_add(self, ctx, member: discord.Member, *, word):
        member_cue_list = []
        member_cue = Mongo.find(self._db, self._coll, {'_id': member.id})
        if member_cue:
            member_cue_list = member_cue['list']
        if word not in member_cue_list:
            Mongo.update(self._db, self._coll, {'_id': member.id},
                         {'$push': {
                             'list': word
                         }})
            await ctx.send(
                f'已新增 {member.display_name} 語錄 {len(member_cue_list) + 1} - {word} <:shiba_smile:783351681013907466>',
                delete_after=7)
            await ctx.message.delete()
            return
        await ctx.send('加過了啦 <:i11_chiwawa:783346447319171075>',
                       delete_after=7)
        await ctx.message.delete()
        return

    @commands.command(
        aliases=['cue_del', 'cue_remove', 'c_d', 'c_r', 'cd', 'cr'])
    async def cue_delete(self, ctx, member: discord.Member, pos: int):
        member_cue_list = []
        member_cue = Mongo.find(self._db, self._coll, {'_id': member.id})
        if member_cue:
            member_cue_list = member_cue['list']
        else:
            await ctx.send(
                f'{member.display_name} 沒有語錄喔 <:shiba_without_ears:783350991885959208>',
                delete_after=7)
            await ctx.message.delete()
            return
        if len(member_cue_list) - 1 <= 0:
            Mongo.delete(self._db, self._coll, {'_id': member.id})
            await ctx.send(
                f'已刪除 {member.display_name} 語錄 {pos} - {member_cue_list[pos - 1]} <:shiba_smile:783351681013907466>',
                delete_after=7)
            await ctx.message.delete()
            return
        if pos > len(member_cue_list):
            await ctx.send(
                f'{member.display_name} 沒有那麼多語錄可以刪啦 <:shiba_without_ears:783350991885959208>',
                delete_after=7)
            await ctx.message.delete()
            return
        member_cue_list = member_cue['list']
        Mongo.update(self._db, self._coll, {'_id': member.id},
                     {'$pull': {
                         'list': member_cue_list[pos - 1]
                     }})
        await ctx.send(
            f'已刪除 {member.display_name} 語錄 {pos} - {member_cue_list[pos - 1]} <:shiba_smile:783351681013907466>',
            delete_after=7)
        await ctx.message.delete()
        return

    @commands.command(aliases=['c_l', 'cl'])
    async def cue_list(self, ctx, member: discord.Member):
        global cue_embed
        if cue_embed:
            await cue_embed[0].delete()
        await ctx.message.delete(delay=3)

        member_cue = None
        member_cue = Mongo.find(self._db, self._coll, {'_id': member.id})
        if not member_cue: return
        total_page = math.ceil(len(member_cue['list']) / 21) - 1

        embed = discord.Embed()
        embed.set_author(name=f'{member.display_name} 錯字大全')
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text=f'頁 {total_page + 1} / {total_page + 1}')

        for i, w in enumerate(member_cue['list'][total_page * 21:],
                              total_page * 21 + 1):
            embed.add_field(name=i, value=w, inline=True)

        cue_embed = [await ctx.send(embed=embed), total_page, member.id]
        await cue_embed[0].add_reaction("<:first_page:806497548343705610>")
        await cue_embed[0].add_reaction("<:prev_page:805002492848767017>")
        await cue_embed[0].add_reaction("<:next_page:805002492525805589>")
        await cue_embed[0].add_reaction("<:last_page:806497548558532649>")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot: return
        if not cue_embed or reaction.message != cue_embed[0]: return
        # await reaction.message.clear_reactions()
        await reaction.remove(user)

        member_cue = None
        member_cue = Mongo.find(self._db, self._coll, {'_id': cue_embed[2]})
        if not member_cue: return
        total_page = math.ceil(len(member_cue['list']) / 21) - 1

        if str(reaction.emoji) == "<:prev_page:805002492848767017>":
            if cue_embed[1] != 0: cue_embed[1] -= 1
        elif str(reaction.emoji) == "<:next_page:805002492525805589>":
            if cue_embed[1] != total_page: cue_embed[1] += 1
        elif str(reaction.emoji) == "<:first_page:806497548343705610>":
            cue_embed[1] = 0
        elif str(reaction.emoji) == "<:last_page:806497548558532649>":
            cue_embed[1] = total_page

        member = (await reaction.message.guild.fetch_member(cue_embed[2]))
        embed = reaction.message.embeds[0]
        embed.clear_fields()
        embed.set_footer(text=f'頁 {cue_embed[1] + 1} / {total_page + 1}')

        for i, w in enumerate(
                member_cue['list'][cue_embed[1] * 21:cue_embed[1] * 21 + 21],
                cue_embed[1] * 21 + 1):
            embed.add_field(name=i, value=w, inline=True)
        await reaction.message.edit(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        global cue_embed
        if not cue_embed: return
        if msg == cue_embed[0]:
            cue_embed = None


def setup(bot):
    bot.add_cog(Cue(bot))
