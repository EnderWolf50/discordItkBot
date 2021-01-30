import discord
from discord.ext import commands
from core.classes import Cog_Ext

import random, os, pymongo, math
from datetime import datetime, timedelta

client = pymongo.MongoClient(
    f"mongodb+srv://Kerati:{os.getenv('MONGO_PASSWORD')}@kerati.o6ymg.mongodb.net/Kerati?retryWrites=true&w=majority"
)

db = client['discord_669934356172636199']
coll = db['cue_list']

prev_list = []

curr_embed = None


class Cue(Cog_Ext):
    @commands.command(aliases=['c'])
    async def cue(self, ctx, member: discord.Member = None, pos: int = None):
        member_cue = None
        if member:
            member_cue = coll.find_one({'_id': member.id})
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
        cue_list = {doc['_id']: doc['list'] for doc in coll.find()}
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
        member_cue = coll.find_one({'_id': member.id})
        if member_cue:
            member_cue_list = member_cue['list']
        if word not in member_cue_list:
            coll.update_one({'_id': member.id}, {'$push': {
                'list': word
            }},
                            upsert=True)
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
        member_cue = coll.find_one({'_id': member.id})
        if member_cue:
            member_cue_list = member_cue['list']
        else:
            await ctx.send(
                f'{member.display_name} 沒有語錄喔 <:shiba_without_ears:783350991885959208>',
                delete_after=7)
            await ctx.message.delete()
            return
        if len(member_cue_list) - 1 <= 0:
            coll.delete_one({'_id': member.id})
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
        coll.update_one({'_id': member.id},
                        {'$pull': {
                            'list': member_cue_list[pos - 1]
                        }})
        await ctx.send(
            f'已刪除 {member.display_name} 語錄 {pos} - {member_cue_list[pos - 1]} <:shiba_smile:783351681013907466>',
            delete_after=7)
        await ctx.message.delete()
        return

    @commands.command(aliases=['c_l', 'cl'])
    async def cue_list(self, ctx, member: discord.Member = None):
        global curr_embed
        member_cue = None
        await ctx.message.delete()
        if curr_embed:
            await curr_embed[0].delete()

        if member:
            member_cue = coll.find_one({'_id': member.id})
        if member_cue:
            member_cue_list = member_cue['list']

            embed = discord.Embed()
            embed.set_author(name=f'{member.display_name} 錯字大全')
            embed.set_thumbnail(url=member.avatar_url)

            for i, w in enumerate(member_cue_list[:21], 1):
                embed.add_field(name=i, value=w, inline=True)

            curr_embed = [await ctx.send(embed=embed), 0, member.id]
            await curr_embed[0].add_reaction("<:L_arrow:805002492848767017>")
            await curr_embed[0].add_reaction("<:R_arrow:805002492525805589>")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        member_cue = None
        if user.bot: return
        if reaction.message != curr_embed[0]: return
        await reaction.remove(user)

        member_cue = coll.find_one({'_id': curr_embed[2]})
        if not member_cue: return
        total_page = math.ceil(len(member_cue['list']) / 21) - 1

        if str(reaction.emoji) == "<:L_arrow:805002492848767017>":
            if curr_embed[1] == 0: return
            curr_embed[1] -= 1
        elif str(reaction.emoji) == "<:R_arrow:805002492525805589>":
            if curr_embed[1] == total_page: return
            curr_embed[1] += 1

        member = (await reaction.message.guild.fetch_member(curr_embed[2]))
        embed = discord.Embed()
        embed.set_author(name=f'{member.display_name} 錯字大全')
        embed.set_thumbnail(url=member.avatar_url)

        for i, w in enumerate(
                member_cue['list'][curr_embed[1] * 21:curr_embed[1] * 21 + 21],
                curr_embed[1] * 21 + 1):
            embed.add_field(name=i, value=w, inline=True)
        await reaction.message.edit(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        global curr_embed
        if not curr_embed: return
        if msg == curr_embed[0]:
            curr_embed = None


def setup(bot):
    bot.add_cog(Cue(bot))
