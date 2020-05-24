import discord
from discord.ext import commands
from core.classes import Cog_Ext

Num_Emoji = [
    "1\N{COMBINING ENCLOSING KEYCAP}",
    "2\N{COMBINING ENCLOSING KEYCAP}",
    "3\N{COMBINING ENCLOSING KEYCAP}",
    "4\N{COMBINING ENCLOSING KEYCAP}",
    "5\N{COMBINING ENCLOSING KEYCAP}",
    "6\N{COMBINING ENCLOSING KEYCAP}",
    "7\N{COMBINING ENCLOSING KEYCAP}",
    "8\N{COMBINING ENCLOSING KEYCAP}",
    "9\N{COMBINING ENCLOSING KEYCAP}"
            ]

Emoji = [
            "\N{REGIONAL INDICATOR SYMBOL LETTER A}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER B}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER C}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER D}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER E}", 
            "\N{REGIONAL INDICATOR SYMBOL LETTER F}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER G}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER H}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER I}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER J}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER K}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER L}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER M}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER N}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER O}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER P}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Q}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER R}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER S}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER T}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER U}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER V}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER W}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER X}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Y}",
            "\N{REGIONAL INDICATOR SYMBOL LETTER Z}"
            ]

class Poll(Cog_Ext):
    @commands.command()
    async def poll(self, ctx, title= None,  *arg):
        if len(arg) <= 20:
            PD = ""
            for i in range(len(arg)):
                PD = PD + "\n" + Emoji[i] + " " + arg[i]
            embed = discord.Embed(description= PD)
            embed_msg = await ctx.send(f"{ctx.author.mention} 發起了投票：\n**「{title}」**", embed= embed)
            for i in range(len(arg)):
                await embed_msg.add_reaction(Emoji[i])
        
        # elif 10 <= len(arg) <= 20:
        #     PD = ""
        #     for i in range(len(arg)):
        #         PD = PD + "\n" + Emoji[i] + " " + arg[i]
        #     embed = discord.Embed(description= PD)
        #     await ctx.send(f"{ctx.author.mention} 發起了投票：\n**{title}**")
        #     embed_msg = await ctx.send(embed = embed)
        #     for i in range(len(arg)):
        #         await embed_msg.add_reaction(Emoji[i])

        else:
            await ctx.send(f"{ctx.author.mention} 反應只能有 20 個 ._.")

def setup(bot):
    bot.add_cog(Poll(bot))