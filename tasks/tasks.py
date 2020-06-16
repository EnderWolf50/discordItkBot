import discord
from core.classes import Cog_Ext

import datetime, asyncio

Three_oclock_Complete = False
Left_three_hours_Complete = False
Left_ten_seconds_Complete = False

class Tasks(Cog_Ext):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        async def Three_oclock():
            global Three_oclock_Complete
            await self.bot.wait_until_ready()
            self.channel = self.bot.get_channel(669934356172636208)
            while not self.bot.is_closed():
                if (datetime.datetime.now() + datetime.timedelta(hours= 8)).strftime("%I") == "03":
                    if not Three_oclock_Complete:
                        Three_oclock_Complete = True
                        Pic = discord.File("Yeah_its_three_oclock.png")
                        await self.channel.send("好棒，三點了", file= Pic)
                    else:
                        pass
                else:
                    Three_oclock_Complete = False
                await asyncio.sleep(1)

        self.Three_oclock_task = self.bot.loop.create_task(Three_oclock())

        async def Left_three_hours():
            global Left_three_hours_Complete
            await self.bot.wait_until_ready()
            self.channel = self.bot.get_channel(669934356172636208)
            while not self.bot.is_closed():
                if (datetime.datetime.now() + datetime.timedelta(hours= 8)).strftime("%w %H") == "0 21":
                    if not Left_three_hours_Complete:
                        Left_three_hours_Complete = True
                        Pic = discord.File("Left_three_hours.jpg")
                        await self.channel.send(file= Pic)
                    else:
                        pass
                else:
                    Left_three_hours_Complete = False
                await asyncio.sleep(1)

        self.Left_three_hours_task = self.bot.loop.create_task(Left_three_hours())

        async def Left_ten_seconds():
            global Left_ten_seconds_Complete
            await self.bot.wait_until_ready()
            self.channel = self.bot.get_channel(669934356172636208)
            while not self.bot.is_closed():
                if (datetime.datetime.now() + datetime.timedelta(hours= 8)).strftime("%w %H %M %S") == "0 23 59 50":
                    if not Left_ten_seconds_Complete:
                        Left_ten_seconds_Complete = True
                        Pic = discord.File("Left_ten_seconds.png")
                        await self.channel.send(file= Pic)
                    else:
                        pass
                else:
                    Left_ten_seconds_Complete = False
                await asyncio.sleep(0.5)

        self.Left_ten_seconds_task = self.bot.loop.create_task(Left_ten_seconds())

def setup(bot):
    bot.add_cog(Tasks(bot))