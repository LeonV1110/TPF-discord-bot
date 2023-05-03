from disnake.ui import View
import disnake

class ExplainEmbedView(View):
    def __init__(self, ):
        super().__init__(timeout=None)
    
    @disnake.ui.button(
        label="Green", style=disnake.ButtonStyle.green, custom_id="persisten_view:green"
    )
    async def green(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        await interaction.response.send_message("")