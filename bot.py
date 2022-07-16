import os
import disnake
from dotenv import load_dotenv
from disnake.ext import commands
import database as db
import whitelistSpreadsheet as ws

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILDID = int(os.getenv('DISCORD_GUILD_ID'))
WHITELISTROLE = int(os.getenv('WHITELIST_ROLE'))

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


@bot.slash_command(description="manually intiates a whitelist update")
async def update_whitelist(inter):
    roles = inter.author.roles
    response = "I wasn't able to find a whitelist role on your user, are you sure that you have connected your patreon to discord?"

    for role in roles:
        if role.id == WHITELISTROLE:
            db.addWhitelist()
            response = "You have recieved whitelist, thanks for suporting us!"
    embed = disnake.Embed(title= response)
    await inter.response.send_message(embed = embed)
    return

@bot.slash_command(description="Checks if anyone has whitelist while not having an appropiate role") #TODO, make sure this is only visable to admins
async def check_freeloaders(inter):
    freeloaders = []
    freeloadersString = ""
    guild = disnake.utils.get(bot.guilds, name = GUILD)
    members = [member for member in guild.members]
    for member in members:
        fullname = member.name + "#" + member.discriminator
        if ws.checkMemberWhitelist(fullname):
            freeloader = True
            for role in member.roles:
                if WHITELISTROLE == role.id:
                    freeloader = False
            if (freeloader):
                freeloaders.append([member.name, member.id])
                freeloadersString +=  "Name: " + member.name + ", Id: " + str(member.id) + "\n"
    embed = disnake.Embed(title=  "Freeloaders:", description=freeloadersString)
    await inter.response.send_message(embed = embed)
    return


@bot.slash_command(description="")
async def test_tpf(inter):
    memberID = inter.author.id
    print(memberID)
    test = inter.author.discriminator
    print(test)
    
    await inter.response.send_message("testing in progress")



bot.run(TOKEN)