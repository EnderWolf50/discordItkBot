import discord
from discord.ext import commands
from core.classes import Cog_Ext

import re, math
from operator import itemgetter

from core.mongo import Mongo

emo_embed = []


class Emo_count(Cog_Ext):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._db = 'discord_669934356172636199'
        self._coll = 'emoji_counter'

    @commands.Cog.listener()
    async def on_ready(self):
        self.mongo_emojis = [
            db_emo['_id'] for db_emo in Mongo.find(self._db, self._coll)
        ]
        self.guild_emojis = [
            g_emo.id for g_emo in (
                await self.bot.fetch_guild(669934356172636199)).emojis
        ]

        for db_emo in self.mongo_emojis:
            if db_emo not in self.guild_emojis:
                Mongo.delete(self._db, self._coll, {'_id': db_emo})
        for g_emo in self.guild_emojis:
            if g_emo not in self.mongo_emojis:
                emo = self.bot.get_emoji(g_emo)
                Mongo.update(self._db, self._coll, {'_id': g_emo}, {
                    "$set": {
                        '_id': g_emo,
                        'name': emo.name,
                        'animated': emo.animated,
                        'count': 0,
                    }
                })

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.channel.type not in {
                discord.ChannelType.text, discord.ChannelType.group
        } or msg.guild.id != 669934356172636199 or msg.author.bot:
            return
        msg_emojis = list(set(re.findall(r'<a?:.*?:(\d*)>', msg.content)))
        for m_emo in msg_emojis:
            Mongo.update(self._db, self._coll, {'_id': int(m_emo)},
                         {'$inc': {
                             'count': 1
                         }})

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        global emo_embed
        if not emo_embed: return
        if msg == emo_embed[0]:
            emo_embed = None

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        if guild.id != 669934356172636199: return

        self.guild_emojis = self.mongo_emojis = [e.id for e in after]
        if len(before) > len(after):
            changed = [e for e in before if e not in after]
            for c_emo in changed:
                Mongo.delete(self._db, self._coll, {'_id': c_emo.id})
        else:
            changed = [e for e in after if e not in before]
            for c_emo in changed:
                Mongo.update(self._db, self._coll, {'_id': c_emo.id}, {
                    '$set': {
                        '_id': c_emo.id,
                        'name': c_emo.name,
                        'animated': c_emo.animated,
                        'count': 0,
                    }
                })

    @commands.command(aliases=['ecr', 'err'])
    async def emo_counter_reset(self, ctx):
        await ctx.message.delete()
        if not (await self.bot.is_owner(ctx.author)): return

        for m_emo in self.mongo_emojis:
            Mongo.update(self._db, self._coll, {
                '_id': m_emo,
            }, {
                '$set': {
                    'name': self.bot.get_emoji(m_emo).name,
                    'count': 0,
                }
            })

    @commands.command(aliases=['er'])
    async def emo_rank(self, ctx, arg=None):
        global emo_embed
        try:
            if emo_embed: await emo_embed[0].delete()
        except:
            pass
        await ctx.message.delete(delay=3)

        db_emo_list = [{
            'id': db_emo['_id'],
            'name': db_emo['name'],
            'animated': db_emo['animated'],
            'count': db_emo['count'],
        } for db_emo in Mongo.find(self._db, self._coll)]
        emo_rank = sorted(db_emo_list, key=itemgetter('count'), reverse=True)
        total_page = math.ceil(len(emo_rank) / 12) - 1

        embed = discord.Embed()
        embed.set_author(name='表符使用率排名 1 ~ 12')
        embed.set_footer(text=f'頁 1 / {total_page + 1}')
        embed.set_thumbnail(url=ctx.guild.icon_url)
        for i, w in enumerate(emo_rank[:12], 1):
            embed.add_field(
                name=i,
                value=
                f"<{'a' if w['animated'] else ''}:{w['name']}:{w['id']}> `{w['count']}`次",
                inline=True)
        emo_embed = [await ctx.send(embed=embed), 0, emo_rank]
        await emo_embed[0].add_reaction("<:first_page:806497548343705610>")
        await emo_embed[0].add_reaction("<:prev_page:805002492848767017>")
        await emo_embed[0].add_reaction("<:next_page:805002492525805589>")
        await emo_embed[0].add_reaction("<:last_page:806497548558532649>")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot: return
        if not emo_embed or reaction.message != emo_embed[0]: return
        # await reaction.message.clear_reactions()
        await reaction.remove(user)

        total_page = math.ceil(len(emo_embed[2]) / 12) - 1

        if str(reaction.emoji) == "<:prev_page:805002492848767017>":
            if emo_embed[1] != 0: emo_embed[1] -= 1
        elif str(reaction.emoji) == "<:next_page:805002492525805589>":
            if emo_embed[1] != total_page: emo_embed[1] += 1
        elif str(reaction.emoji) == "<:first_page:806497548343705610>":
            emo_embed[1] = 0
        elif str(reaction.emoji) == "<:last_page:806497548558532649>":
            emo_embed[1] = total_page

        embed = reaction.message.embeds[0]
        embed.clear_fields()
        embed.set_author(
            name=f'表符使用率排名 {emo_embed[1] * 12 + 1} ~ {emo_embed[1] * 12 + 12}')
        embed.set_footer(text=f'頁 {emo_embed[1] + 1} / {total_page + 1}')

        for i, w in enumerate(
                emo_embed[2][emo_embed[1] * 12:emo_embed[1] * 12 + 12],
                emo_embed[1] * 12 + 1):
            embed.add_field(
                name=i,
                value=
                f"<{'a' if w['animated'] else ''}:{w['name']}:{w['id']}> `{w['count']}`次",
                inline=True)
        await reaction.message.edit(embed=embed)


def setup(bot):
    bot.add_cog(Emo_count(bot))
