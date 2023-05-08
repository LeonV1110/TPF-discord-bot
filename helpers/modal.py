import disnake
from disnake.ext import commands
from disnake import TextInputStyle
from disnake.interactions.modal import ModalInteraction
from disnake.ui import Modal, TextInput

class RegisterModal(Modal):
    def __init__(self, inter_id):
        components = [
            TextInput(
            label= 'Steam64ID', 
            placeholder='76561198029817168', 
            custom_id="inter_id", 
            style=TextInputStyle.short, 
            max_length=19)]
        super().__init__(title='Register', components=components, custom_id="inter_id", timeout=600)
    
    async def callback(self, inter: ModalInteraction):
        print('AARDAPPEL')
        embed = disnake.Embed(title='Registration')
        for key, value in inter.text_values.items():
            print('Modal: Key: ' + str(key) + ' Value: ' + str(value))
            pass #Do registration
        await inter.response.send_message(embed=embed)

    async def on_error(self, error: Exception, inter: ModalInteraction):
        await inter.response.send_message(error)