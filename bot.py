import os
import disnake
from dotenv import load_dotenv
from disnake.ext import commands
from numpy import true_divide
import database as db
import whitelistSpreadsheet as ws
import pandas as pd

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILDID = int(os.getenv('DISCORD_GUILD_ID'))
WHITELISTROLE = int(os.getenv('WHITELIST_ROLE'))

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(intents = intents, command_prefix='/')

#log in the bot
@bot.event
async def on_ready():
    print(f"We're logged in as {bot.user}")

#
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
    
    toCheck = []
    hasWhitelistrole = []
    for member in members:
        discordName = member.name + "#" + member.discriminator
        toCheck.append(discordName)
        for role in member.roles:
            if WHITELISTROLE == role.id:
                hasWhitelistrole.append(discordName)

    hasWhitelist = ws.checkListWhitelist(toCheck)

    for user in hasWhitelist:
        if (not (user in hasWhitelistrole)):
            freeloaders.append([member.name, member.id])
            freeloadersString +=  "Name: " + user

    if (len(freeloaders) == 0):
        embeded = disnake.Embed(title = "No Freeloaders detected!")
    else:
        embeded = disnake.Embed(title=  "Freeloaders:", description=freeloadersString)

    await inter.followup.send(embed = embeded)
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

@bot.slash_command(description="")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def link_name_to_dis_id(inter):
    users = ws.getUsernameSteamIDDisID() #Pandas dataframe
    guild = disnake.utils.get(bot.guilds, name = GUILD)
    members = [member for member in guild.members]
    print (users)
    #TODO
    return

@bot.slash_command(description="checks how many people are whitelisted in the sheet")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def count_whitelist(inter):
    res = ws.countWhitelist()
    embed = disnake.Embed(title = "We currently have " + str(res) + " people in the whitelist document")
    await inter.response.send_message(embed = embed)
    return

bot.run(TOKEN)