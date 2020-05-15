import discord
from discord.ext import commands
from core.classes import Cog_Ext

Repeat_Cmd_status = False
Cannot_delete = False

class Repeat(Cog_Ext):
    @commands.command()
    async def repeat(self, ctx):
        if ctx.author == self.bot.get_user(523755296242270210) or ctx.author == self.bot.get_user(590430031281651722):
            global Repeat_Cmd_status
            Repeat_Cmd_status = not Repeat_Cmd_status
            if Repeat_Cmd_status == True:
                await ctx.send(">> 複讀功能**啟用** <:emoji_150:689498513838440471>")
            else:
                await ctx.send(">> 複讀功能**關閉** <:emoji_26:685774183971815516>")

    @commands.command()
    async def cnd(self, ctx):
        if ctx.author == self.bot.get_user(523755296242270210) or ctx.author == self.bot.get_user(590430031281651722):
            global Cannot_delete
            Cannot_delete = not Cannot_delete

    @commands.Cog.listener()
    async def on_message_delete(self, msg):
        if Repeat_Cmd_status == True:
            if Cannot_delete == False:
                if msg.author != self.bot.user:
                    if msg.content.startswith(">"):
                        await msg.channel.send(msg.author.mention + "：\n" + msg.content)
                    else:
                        await msg.channel.send(msg.author.mention + "：" + msg.content)
            else:
                if msg.content.startswith(">"):
                    await msg.channel.send(msg.author.mention + "：\n" + msg.content)
                else:
                    await msg.channel.send(msg.author.mention + "：" + msg.content)

def setup(bot):
    bot.add_cog(Repeat(bot))