import discord
from discord.ext import commands
from core.classes import Cog_Ext
from core.rwFile import get_setting

Owner = get_setting("Owner")

class Basic(Cog_Ext):
    @commands.command()
    async def load(self, ctx, folder, extension):
        if ctx.author == self.bot.get_user(Owner):
            self.bot.load_extension(f"{folder}.{extension}")
            await ctx.message.delete()
            await ctx.send(f"**{extension}** has been loaded!", delete_after= 3)

    @commands.command()
    async def unload(self, ctx, folder, extension):
        if ctx.author == self.bot.get_user(Owner):
            self.bot.unload_extension(f"{folder}.{extension}")
            await ctx.message.delete()
            await ctx.send(f"**{extension}** has been unloaded!", delete_after= 3)

    @commands.command()
    async def reload(self, ctx, folder, extension):
        if ctx.author == self.bot.get_user(Owner):
            self.bot.reload_extension(f"{folder}.{extension}")
            await ctx.message.delete()
            await ctx.send(f"**{extension}** has been reloaded!", delete_after= 3)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Ping is {round(self.bot.latency*1000)} ms and... Pong!')

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title= "Command Help", color= 0xfda34e)
        embed.set_author(name= "Itk Bot", icon_url= "https://cdn.discordapp.com/avatars/710498084194484235/e91dbe68bd05239c050805cc060a34e9.webp?size=128")
        embed.add_field(name= "bzz", value= "抽籤！", inline= True)
        embed.add_field(name= "tdbzz", value= "當日運勢", inline= True)
        embed.add_field(name= "choose (...)", value= "協助選擇障礙患者做出決定 ouo", inline= True)
        embed.add_field(name= "poll|vote <標題> (選項...)", value= "發起投票", inline= True)
        await ctx.send(embed= embed)

def setup(bot):
    bot.add_cog(Basic(bot))