import os
import disnake
from dotenv import load_dotenv
from disnake.ext import commands
from numpy import true_divide
import database as db
import whitelistSpreadsheet as ws
import pandas as pd
import helper as hlp
import player as pl
import errors as err

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILDID = int(os.getenv('DISCORD_GUILD_ID'))
WHITELISTROLE = int(os.getenv('WHITELIST_ROLE'))

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(intents = intents, command_prefix='/')

#logs in the bot
@bot.event
async def on_ready():
    print(f"We're logged in as {bot.user}")

#########################################
########   Player Commands    ###########
#########################################
#TODO, make available to everyone

#enters the user into the database, if already present it will let the user know
@bot.slash_command(discription = "Link your steam64ID with your discord account in our database")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def register(inter, steam64id: str):
        await inter.response.defer()
        checkID = hlp.checkSteam64ID(steam64id)
        if (not checkID =="suc6"):
            embed = disnake.Embed(title = checkID)
            await inter.followup.send(embed = embed)
            return
        
        steam64ID = int(steam64id)
        discordID = inter.author.id
        whitelist = False
        roles = inter.author.roles        
        for role in roles:
            if role.id == WHITELISTROLE:
                whitelist = True
        try: 
            hlp.checkDuplicateUser(steam64ID, discordID)
        except err.DuplicatePlayerPresent:
            embed = disnake.Embed(title = "There already exists a user with your steam64ID or discordID")
            await inter.followup.send(embed = embed)
            return
        player = pl.DiscordPlayer(discordID= discordID, steam64ID=steam64ID, whitelist= whitelist)
        player.playerToDB()
        embed = disnake.Embed(title = "Registration was sucessfull")
        await inter.followup.send(embed = embed)


#updates the whitelist of the user using it
@bot.slash_command(description="manually intiates a whitelist update")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def update_whitelist(inter):
    discordID = inter.author.id
    player = pl.DatabasePlayer(discordID)
    roles = inter.author.roles
    response = "I wasn't able to find a whitelist role on your user, are you sure that you have connected your patreon to discord?"

    for role in roles:
        if role.id == WHITELISTROLE:
            player.updateWhitelist(True)
            response = "You have recieved whitelist, thanks for suporting us!"
    embed = disnake.Embed(title= response)
    await inter.response.send_message(embed = embed)
    return

#########################################
########   Admin Commands    ############
#########################################

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

#########################################
#######   testing Commands    ###########
#########################################

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

@bot.slash_command(description="checks how many people are whitelisted in the sheet")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def count_whitelist(inter):
    res = ws.countWhitelist()
    embed = disnake.Embed(title = "We currently have " + str(res) + " people in the whitelist document")
    await inter.response.send_message(embed = embed)
    return

bot.run(TOKEN)