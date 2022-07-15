from contextlib import nullcontext
from string import ascii_uppercase
import os
import disnake
from dotenv import load_dotenv
from disnake.ext import commands
import database as db

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILDID = int(os.getenv('DISCORD_GUILD_ID'))
WHITELISTROLE = os.getenv('WHITELIST_ROLE')

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

@bot.slash_command(description="Link your steam64ID with your discord account in our database")
async def register(inter, steam64id: int):
    print (steam64id)
    #await do something in a database
    await inter.response.send_message("suc6")


@bot.slash_command(description="")
async def update_whitelist(inter):
    roles = inter.author.roles
    print(roles)
    if WHITELISTROLE in roles: #TODO, doesn't work atm
        await db.addWhitelist
        await inter.response.send_message("You have recieved whitelist, thanks for suporting us!")
    else:
        await inter.response.send_message("I wasn't able to find a whitelist role on your user, are you sure that you have connected your patreon to discord?")

@bot.slash_command(description="")
async def test_tpf(inter):
    memberID = inter.author.id
    
    print(memberID)
    await inter.response.send_message("testing in progress")


bot.run(TOKEN)