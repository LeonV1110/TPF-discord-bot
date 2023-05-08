from disnake.ui import View
import disnake

class ExplainEmbedView(View):
    def __init__(self):
        super().__init__(timeout=None)