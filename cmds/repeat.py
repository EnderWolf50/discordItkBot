import discord
from discord.ext import commands
from core.classes import Cog_Ext
from core.rwFile import get_setting

Owner = get_setting("Owner")
Traveler = get_setting("Traveler")

Repeat_cmd_status = False
Cannot_delete = False
Edit_repeat = False
Edit_record = {}


class Repeat(Cog_Ext):
    @commands.command()
    async def repeat(self, ctx):
        await ctx.message.delete()
        if ctx.author == self.bot.get_user(
                Owner) or ctx.author == self.bot.get_user(Traveler):
            global Repeat_cmd_status
            Repeat_cmd_status = not Repeat_cmd_status
            if Repeat_cmd_status == True:
                await ctx.author.send(
                    ">> 複讀功能**啟用** <:emoji_150:689498513838440471>")
            else:
                await ctx.author.send(
                    ">> 複讀功能**關閉** <:emoji_26:685774183971815516>")

    @commands.command()
    async def editr(self, ctx):
        await ctx.message.delete()
        if ctx.author == self.bot.get_user(
                Owner) or ctx.author == self.bot.get_user(Traveler):
            global Edit_repeat
            Edit_repeat = not Edit_repeat
            if Edit_repeat == True:
                await ctx.author.send(
                    ">> 編輯歷程**啟用** <:emoji_150:689498513838440471>")
            else:
                await ctx.author.send(
                    ">> 編輯歷程**關閉** <:emoji_26:685774183971815516>")

    @commands.command()
    async def cnd(self, ctx):
        await ctx.message.delete()
        if ctx.author == self.bot.get_user(
                Owner) or ctx.author == self.bot.get_user(Traveler):
            global Cannot_delete
            Cannot_delete = not Cannot_delete
            if Cannot_delete:
                await ctx.author.send("CanNotDelete Mode: On")
            else:
                await ctx.author.send("CanNotDelete Mode: Off")

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        if Repeat_cmd_status == True:
            if Cannot_delete == False:
                if msg.author != self.bot.user:
                    if msg.content.startswith(">"):
                        await msg.channel.send(msg.author.mention + "：\n" +
                                               msg.content)
                    else:
                        await msg.channel.send(msg.author.mention + "：" +
                                               msg.content)
            else:
                if msg.content.startswith(">"):
                    await msg.channel.send(msg.author.mention + "：\n" +
                                           msg.content)
                else:
                    await msg.channel.send(msg.author.mention + "：" +
                                           msg.content)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author != self.bot.user:
            if Edit_repeat == True:
                await before.channel.send(before.author.mention + "：" +
                                          before.content + " → " +
                                          after.content)
        # edit backup
        if before.author.bot: return
        if before.content == after.content: return
        if str(before.id) not in Edit_record.keys():
            Edit_record[f'{before.id}'] = 0
        print(2)
        Edit_record[f'{before.id}'] += 1
        await self.bot.get_channel(745569697013039105).send(
            f'{before.author.display_name}  `{after.edited_at.strftime("%Y/%m/%d %H:%M:%S")}` `{Edit_record[f"{before.id}"]}`\n{before.content} → {after.content}'
        )


def setup(bot):
    bot.add_cog(Repeat(bot))