from typing import Optional
from disnake.ext import commands
from disnake import Intents


class PersistentBot(commands.bot):
    def __init__(self):
        intents = Intents.default()
        intents.members = True
        intents.message_content = True #TODO, probably not needed
        super().__init__(intents = intents, command_prefix='/')
        self.persistent_views_added = False
    





bot = PersistentBot()