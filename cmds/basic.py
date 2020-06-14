import discord
from discord.ext import commands
from core.classes import Cog_Ext
from core.rwFile import get_setting, rFile

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
    async def help(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title= "Command Help", color= 0xfda34e)
        embed.set_author(name= "Itk Bot", icon_url= "https://cdn.discordapp.com/avatars/710498084194484235/e91dbe68bd05239c050805cc060a34e9.webp?size=128")
        embed.set_footer(text= "那個...窩不知道")
        for command, description, inline in rFile("others")["help"]:
            embed.add_field(name= command, value= description, inline= inline)
        await ctx.send(embed= embed)

    @commands.command()
    async def close(self, ctx):
        await self.bot.close()

def setup(bot):
    bot.add_cog(Basic(bot))