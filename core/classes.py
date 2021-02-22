import discord
from discord.ext import commands

import os, pymongo, logging


class Cog_Ext(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.mongo_client = pymongo.MongoClient(
            f"mongodb+srv://Kerati:{os.getenv('MONGO_PASSWORD')}@kerati.o6ymg.mongodb.net/Kerati?retryWrites=true&w=majority"
        )
