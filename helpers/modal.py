import disnake
from disnake.ext import commands
from disnake import TextInputStyle
from disnake.interactions.modal import ModalInteraction
from disnake.ui import Modal, TextInput
from helpers.botHelper import register_player
from helpers.error import MyException
from pymysql import OperationalError
class RegisterModal(Modal):
    def __init__(self, inter_id):
        components = [
            TextInput(
            label= 'Please provide your Steam64ID for registration.', 
            placeholder='76561198029817168', 
            custom_id=str(inter_id), 
            style=TextInputStyle.short, 
            max_length=19)]
        super().__init__(title='Register', components=components, custom_id=str(inter_id), timeout=600)
    
    async def callback(self, inter: ModalInteraction):
        embed = disnake.Embed(title='Registration')
        response = inter.text_values.items()
        key, value = response[0]
        try:
            register_player(member=inter.author, steam64ID=value)
        except MyException as error:
            embed = disnake.Embed(title=error.message)
        except OperationalError:
            embed = disnake.Embed(
            title="The bot is currently having issues, please try again later.")
        await inter.response.send_message(embed=embed, ephemeral=True)

    async def on_error(self, error: Exception, inter: ModalInteraction):
        await inter.response.send_message(error)