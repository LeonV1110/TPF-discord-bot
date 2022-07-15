from string import ascii_uppercase
import os
import disnake
from dotenv import load_dotenv
from disnake.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILDID = int(os.getenv('DISCORD_GUILD_ID'))

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(intents = intents, command_prefix='/')

@bot.event
async def on_ready():
    print(f"We're logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content == "hello":
        await message.channel.send('Hello!')

@bot.slash_command(description="Responds with 'World'")
async def register(inter, steam64id):
    print (steam64id)
    await inter.response.send_message("suc6")

bot.run(TOKEN)