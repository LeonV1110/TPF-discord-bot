import os
import disnake
from dotenv import load_dotenv
from disnake.ext import commands
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

#update whitelist when roles change
@bot.event
async def on_member_update(before, after):
    hlp.updateWhitelist(after)

#remove whitelist when they leave the server
@bot.event #TODO test
async def on_member_remove(member):
    try:
        player = pl.DatabasePlayer(member.id)
        player.updateWhitelist(False)
    except err.PlayerNotFound:
        return

#########################################
########   Player Commands    ###########
#########################################
#TODO, make available to everyone

#enters the user into the database, if already present it will let the user know
@bot.slash_command(discription = "Link your steam64ID with your discord account in our database")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def register(inter, steam64id: str):
        await inter.response.defer(ephemeral = True)
        steam64ID = int(steam64id)
        discordID = inter.author.id
        whitelist = False
        roles = inter.author.roles 
        name = inter.author.name + "#" + inter.author.discriminator
        for role in roles:
            if role.id == WHITELISTROLE:
                whitelist = True
        try:
            player = pl.DiscordPlayer(discordID= discordID, steam64ID=steam64ID, whitelist= whitelist, name = name)
        except err.InvalidSteam64ID as error:
            embed = disnake.Embed(title= error.message)
            await inter.followup.send(embed = embed, ephemeral = True)
            return
        
        try: 
            player.playerToDB()
        except err.DuplicatePlayerPresent:
            embed = disnake.Embed(title = "There already exists a user with your steam64ID or discordID")
            await inter.followup.send(embed = embed, ephemeral = True)
            return
        
        
        embed = disnake.Embed(title = "Registration was successful")
        await inter.followup.send(embed = embed, ephemeral = True)


#updates the whitelist of the user using it
@bot.slash_command(description="manually intiates a whitelist update")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def update_whitelist(inter):
    member = inter.author
    response = hlp.updateWhitelist(member)
    embed = disnake.Embed(title= response)
    await inter.response.send_message(embed = embed, ephemeral = True)
    return

#removes a players own entry from the database
@bot.slash_command(description="Deletes your entry from our database, this will also remove your whitelist.")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def remove_from_database(inter):
    discordID = inter.author.id
    try:
        player = pl.DatabasePlayer(discordID)
    except err.PlayerNotFound:
        embed = disnake.Embed(title = "You weren't in the database to begin with")
        await inter.response.send_message(embed = embed, ephemeral = True)
        return
    player.deletePlayerFromDB()
    embed = disnake.Embed(title="You have been successfully deleted from the database")
    await inter.response.send_message(embed = embed, ephemeral = True)

#########################################
########   Admin Commands    ############
#########################################

@bot.slash_command(description="Updates all whitelists for everyone")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def update_all_whitelists(inter):
    guild = disnake.utils.get(bot.guilds, name = GUILD)
    members = [member for member in guild.members]
    hasWhitelistrole = []
    for member in members:
        for role in member.roles:
            if WHITELISTROLE == role.id:
                try: 
                    player = pl.DatabasePlayer(member.id)
                    player.updateWhitelist(True)
                except err.PlayerNotFound:
                    print(member.name +"#" + member.discriminator + " was not found in the database")
                    return
            else:
                try: 
                    player = pl.DatabasePlayer(member.id)
                    player.updateWhitelist(False)
                except err.PlayerNotFound:
                    print(member.name +"#" + member.discriminator + " was not found in the database")
                    return
    return

@bot.slash_command(description="Checks in the spreadsheet if anyone has whitelist while not having an appropiate role")
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

    await inter.followup.send(embed = embeded, ephemeral = True)
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
    new = await inter.followup(ephemeral = True)
    await new.response.send_message("test")
    return

@bot.slash_command(description="checks how many people are whitelisted in the sheet")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def count_whitelist(inter):
    res = ws.countWhitelist()
    embed = disnake.Embed(title = "We currently have " + str(res) + " people in the whitelist document")
    await inter.response.send_message(embed = embed)
    return

@bot.slash_command(description="imports the old players in the spreadsheet to the database")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def import_from_spreadsheet(inter):
    await inter.response.defer()

    df = ws.opensheet()
    length = len(df)
    nameSeries = df['discord username'].squeeze()
    steam64IDSeries = df['steamid'].squeeze()
    discordIDSeries = df['DiscordID'].squeeze()
    group = df['group']

    for i in range(length):
        if (group.at[i] == 'whitelist'):
            name = nameSeries.at[i]
            discordID = discordIDSeries.at[i]
            steam64ID = steam64IDSeries.at[i]
            #print(type(discordID))
            if (isinstance(discordID, int)):
                print(discordID)
                try:
                    player = pl.DiscordPlayer(discordID, steam64ID, True, name)
                    player.playerToDB()
                except: 
                    pass
    embed = disnake.Embed(title="Did something, may have crashed regardless")
    await inter.followup.send(embed = embed)
            #TODO, allow for people to be missing their discordID
    return

@bot.slash_command(description="add the discordID to anyone in the spreadsheet")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def update_discordid_spreadsheet(inter):
    await inter.response.defer()
    wks = ws.openWks()
    guild = disnake.utils.get(bot.guilds, name = GUILD)
    members = [member for member in guild.members]
    hasWhitelistrole = []
    for member in members:
        for role in member.roles:
            if WHITELISTROLE == role.id:
                hasWhitelistrole.append(member)

    for member in hasWhitelistrole:
        discordName = member.name + "#" + member.discriminator
        discordID = member.id
        ws.updateDiscordID(wks, discordName, discordID)
    embed = disnake.Embed(title= "Updated")
    await inter.followup.send(embed = embed)

    return
bot.run(TOKEN)