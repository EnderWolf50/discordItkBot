import discord
from discord.ext import commands

import os, pymongo


class Cog_Ext(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mongo_client = pymongo.MongoClient(
            f"mongodb+srv://Kerati:{os.getenv('MONGO_PASSWORD')}@kerati.o6ymg.mongodb.net/Kerati?retryWrites=true&w=majority"
        )

    def get_mongo_client(self):
        return self.mongo_client
