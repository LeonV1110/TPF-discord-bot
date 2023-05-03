from typing import Optional
from disnake.ext import commands
from disnake import Intents


class PersistentBot(commands.bot):
    def __init__(self, intents, command_prefix):
        super().__init__(intents = intents, command_prefix=command_prefix)
        self.persistent_views_added = False
    




intents = Intents.default()
intents.members = True
intents.message_content = True #TODO, probably not needed
bot = PersistentBot(intents = intents, command_prefix='/')