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
"""
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if message.content == "hello":
        await message.channel.send('Hello!')
"""

@bot.slash_command(description="Link your steam64ID with your discord account in our database")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def register(inter, steam64id: int):
    print (steam64id)
    #await do something in a database
    await inter.response.send_message("suc6")


@bot.slash_command(description="manually intiates a whitelist update")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
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
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def check_freeloaders(inter):

    await inter.response.defer()

    freeloaders = []
    freeloadersString = ""
    guild = disnake.utils.get(bot.guilds, name = GUILD)
    members = [member for member in guild.members]
    for member in members:
        fullname = member.name + "#" + member.discriminator
        print(fullname)
        if ws.checkMemberWhitelist(fullname):
            freeloader = True
            for role in member.roles:
                if WHITELISTROLE == role.id:
                    freeloader = False
            if (freeloader):
                freeloaders.append([member.name, member.id])
                freeloadersString +=  "Name: " + member.name + ", Id: " + str(member.id) + "\n"
    embeded = disnake.Embed(title=  "Freeloaders:", description=freeloadersString)

    await inter.followup.send(freeloadersString)

    print(freeloader)
    return


@bot.slash_command(description="")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def test_tpf(inter):
    memberID = inter.author.id
    print(memberID)
    test = inter.author.discriminator
    print(test)
    
    await inter.response.send_message("testing in progress")

@bot.slash_command(description="")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def get_whitelist_id(inter):
    print(inter.author.roles)
    await inter.response.send_message("test")
    print(inter.token)
    #await inter.response.defer()
    new = await inter.followup()
    await new.response.send_message("test")
    #await inter.followup.send("Done")
    return

bot.run(TOKEN)