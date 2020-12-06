import discord
from discord.ext import commands
from core.classes import Cog_Ext

import random, os, pymongo
from datetime import datetime, timedelta

client = pymongo.MongoClient(
    f"mongodb+srv://Kerati:{os.getenv('MONGO_PASSWORD')}@kerati.o6ymg.mongodb.net/Kerati?retryWrites=true&w=majority"
)

db = client['discord_669934356172636199']
coll = db['cue_list']

prev_list = None
curr_list = None


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
                    f'{member.mention} 語錄 {pos} - {member_cue_list[pos - 1]}')
                await ctx.message.delete()
                return
            word = random.choice(member_cue_list)
            await ctx.send(
                f'{member.mention} 語錄 {member_cue_list.index(word) + 1} - {word}'
            )
            await ctx.message.delete()
            return
        cue_list = {doc['_id']: doc['list'] for doc in coll.find()}
        random_cue_id = random.choice(list(cue_list.keys()))
        random_member = self.bot.get_user(random_cue_id)
        random_pos = random.randint(0, len(cue_list[random_cue_id]) - 1)
        random_word = cue_list[random_cue_id][random_pos]
        await ctx.send(
            f'{random_member.mention} 語錄 {random_pos} - {random_word}')
        await ctx.message.delete()
        return

    @commands.command()
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
                f'已新增 {member.nick} 語錄 {len(member_cue_list) + 1} - {word} <:shiba_smile:783351681013907466>',
                delete_after=7)
            await ctx.message.delete()
            return

    @commands.command(aliases=['cue_del', 'cue_remove'])
    async def cue_delete(self, ctx, member: discord.Member, pos: int):
        member_cue_list = []
        member_cue = coll.find_one({'_id': member.id})
        if not member_cue:
            await ctx.send(f'{member.nick} 沒有語錄喔 <:shiba_without_ears:783350991885959208>',
                           delete_after=7)
            await ctx.message.delete()
            return
        if len(member_cue_list) - 1 == 0:
            coll.delete_one({'_id': member.id})
            await ctx.send(
            f'已刪除 {member.nick} 語錄 {pos} - {member_cue_list[pos - 1]} <:shiba_smile:783351681013907466>',
            delete_after=7)
            await ctx.message.delete()
            return
        if pos > len(member_cue_list):
            await ctx.send(f'{member.nick} 沒有那麼多語錄可以刪啦 <:shiba_without_ears:783350991885959208>',
                           delete_after=7)
            await ctx.message.delete()
            return
        member_cue_list = member_cue['list']
        coll.update_one({'_id': member.id},
                        {'$pull': {
                            'list': member_cue_list[pos - 1]
                        }})
        await ctx.send(
            f'已刪除 {member.nick} 語錄 {pos} - {member_cue_list[pos - 1]} <:shiba_smile:783351681013907466>',
            delete_after=7)
        await ctx.message.delete()
        return

    @commands.command()
    async def cue_list(self, ctx, member: discord.Member = None):
        if member:
            member_cue_list = coll.find_one({'_id': member.id})['list']

            msg = f'{member.nick}\n'
            for i, w in enumerate(member_cue_list, 1):
                msg += f'{i} - {w}\n'
            await ctx.send(msg)
            await ctx.message.delete()
            return
        global prev_list
        global curr_list
        if prev_list:
            await prev_list.delete()
        cue_list = {doc['_id']: doc['list'] for doc in coll.find()}
        msg = ''
        for m, l in cue_list.items():
            cue_member = ctx.guild.get_member(m)
            msg += f'{cue_member.nick}\n'
            for i, w in enumerate(l, 1):
                msg += f'{i} - {w}\n'
        prev_list = await ctx.send(msg)
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(Cue(bot))
