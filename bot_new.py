import os
import disnake
from dotenv import load_dotenv
from disnake.ext import commands
import pandas as pd
import helper_new as hlp
import player_new as pl
import errors_new as err
import whitelistSpreadsheet as ws
import database_new as db
import whitelistDoc as wd
import WhitelistOrder as wo

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILDID = int(os.getenv('DISCORD_GUILD_ID'))
WHITELISTROLE = int(os.getenv('WHITELIST_ROLE'))

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(intents = intents, command_prefix='/')

######################
###### events ########
######################

#print msg when the bot is logged in
@bot.event
async def on_ready():
    print(f"We're logged in as {bot.user}")

#update whitelistorder tier when roles change 
@bot.event
async def on_member_update(before, after):
    member = after
    hlp.updateWhitelist(member)

#remove whitelist when they leave the server
@bot.event
async def on_member_remove(member):
    try:
        player = pl.DatabasePlayer(member.id)
        TPFID = player.TPFID
        try:
            order = wo.DatabaseOrder(TPFID)
            order.updateOrderTier(member.roles) #TODO, make sure it works
        except err.OrderNotFound() as error:
            return error.message
    except err.PlayerNotFound:
        return error.message

#########################################
########   Player Commands    ###########
#########################################
#TODO, make available to everyone

#enters the user into the database, if already present it will let the user know
@bot.slash_command(discription = "Link your steam64ID with your discord account in our database")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def register(inter, steam64id: str):
    await inter.response.defer(ephemeral = True)
    discordID = inter.author.id
    role = inter.author.roles
    name = inter.author.name + "#" + inter.author.discriminator

    embed = disnake.Embed(title = "Registration was successful")
    try:
        player = pl.NewPlayer(discordID, steam64id, role, name)
    except (err.InvalidSteam64ID, err.InvalidRole ) as error:
        embed = disnake.Embed(title= error.message)
        await inter.followup.send(embed = embed, ephemeral = True)
        return
    try:
        player.playerToDB()
    except err.DuplicatePlayerPresent as error2:
        embed = disnake.Embed(title = error2.message)

    await inter.followup.send(embed = embed, ephemeral = True)

#updates the role of the user using it
@bot.slash_command(description="manually intiates a whitelist update")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def update_my_whitelist(inter):
    member = inter.author
    response = hlp.updateWhitelist(member)
    embed = disnake.Embed(title= response)
    await inter.response.send_message(embed = embed, ephemeral = True)
    return

#removes a players own entry from the database
@bot.slash_command(description="Deletes your entry from our database, this will also remove your whitelist.")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def remove_myself_from_database(inter):
    discordID = inter.author.id
    try:
        player = pl.DatabasePlayer(discordID)
        player.deletePlayer()
    except err.PlayerNotFound as error:
        embed = disnake.Embed(title = error.message)
        await inter.response.send_message(embed = embed, ephemeral = True)
        return
    
    embed = disnake.Embed(title="You have been successfully deleted from the database")
    await inter.response.send_message(embed = embed, ephemeral = True)
    return

#########################################
########   Admin Commands    ############
#########################################

#removes a specified players entry from the database
@bot.slash_command(description="Deletes your entry from our database, this will also remove your whitelist.")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def nuke_player(inter, discordid : str, steam64id : str):
    try:
        player = pl.DatabasePlayer(discordid)
        if int(player.steam64ID) != int(steam64id):
            embed = disnake.Embed(title = "No matching player found")
            await inter.response.send_message(embed = embed)
            return
        player.deletePlayer()
    except err.PlayerNotFound as error:
        embed = disnake.Embed(title = error.message)
        await inter.response.send_message(embed = embed)
        return
    
    embed = disnake.Embed(title="This player has been successfully deleted from the database")
    await inter.response.send_message(embed = embed)


#TODO
@bot.slash_command(description="Updates all roles for everyone")
@commands.default_member_permissions(kick_members=True, manage_roles=True, administrator = True)
async def update_all_whitelists(inter):
    await inter.response.defer()
    
    guild = disnake.utils.get(bot.guilds, name = GUILD)
    members = [member for member in guild.members]

    for member in members:
        role = "nothing"
        for discordRole in member.roles:
            if WHITELISTROLE == discordRole.id:
                role = "whitelist"
        try:
            player = pl.DatabasePlayer(member.id)
            player.updateRoleNoDoc(role)
        except err.PlayerNotFound as error:
            if role =="whitelist":
                print(member.name +"#" + member.discriminator + " raised exception: " + error.message)
    wd.createWhitelistDoc()
    embed = disnake.Embed(title = "Done")
    await inter.followup.send(embed = embed)
    return

#TODO, check and maybe rewrite, will be deprecated soon though
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
    i = 0
    for user in hasWhitelist:
        if (not (user in hasWhitelistrole)):
            i +=1
            freeloaders.append([member.name, member.id])
            freeloadersString +=  str(i) + " - Name: " + user + '\n'

    if (len(freeloaders) == 0):
        embeded = disnake.Embed(title = "No Freeloaders detected!")
    else:
        embeded = disnake.Embed(title=  "Freeloaders:", description=freeloadersString)

    await inter.followup.send(embed = embeded, ephemeral = True)
    return

@bot.slash_command(description="Checks in the spreadsheet if anyone has whitelist while not having an appropiate role")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def import_spreadsheet(inter):
    await inter.response.defer() 
    df = ws.opensheet()

    length = len(df)
    nameSeries = df['discord username'].squeeze()
    steam64IDSeries = df['steamid'].squeeze()
    discordIDSeries = df['DiscordID'].squeeze()
    groupSeries = df['group']

    AllowedGroups = ['whitelist', 'mvp', 'creator', 'caster' ]
    count = 0

    guild = disnake.utils.get(bot.guilds, name = GUILD)
    members = [member for member in guild.members]

    for i in range(length):
        group = groupSeries.at[i]
        if (group in AllowedGroups):
            name = nameSeries.at[i]
            discordID = discordIDSeries.at[i]
            steam64ID = steam64IDSeries.at[i]
            if (isinstance(discordID, int)):
                try:
                    player = pl.SpreadsheetPlayer(discordID, steam64ID, group, name)
                    player.playerToDB()
                    try:
                        for member in members:
                            if member.id == discordID:
                                roles = member.roles
                                wlOrder = wo.NewOrder(discordID, roles)
                                wlOrder.orderToDB()

                                player.updatePermission(roles)

                    except err.InvalidRole as error:
                        print(name + " Has no whitelist role")
                        pass
                except err.DuplicatePlayerPresent:
                    pass
                except (err.PlayerNotFound, err.InvalidSteam64ID) as error: 
                    print(discordID + ' ' +  name)
                    print(error.message)
            else:
                count += 1
                print (steam64ID)
                print("No discordID")
        
    print(str(count) + " missing discordID's")
    await inter.followup.send("Spreadsheet has been imported")
    return

#########################################
#######   testing Commands    ###########
#########################################

#used during development, changes to whats needed
@bot.slash_command(description="")
@commands.default_member_permissions(kick_members=True, manage_roles=True, administrator = True)
async def test_tpf(inter):
    memberID = inter.author.id
    print(memberID)
    test = inter.author.discriminator
    print(test)
    await inter.response.send_message("testing in progress")
    await inter.followup.send("more testing")

#########################
####### Setup ###########
#########################

@bot.slash_command(description="Only run once!, sets up the database and imports from the spreadsheet")
@commands.default_member_permissions(kick_members=True, manage_roles=True, administrator = True)
async def setup(inter):
    await inter.response.defer() 
    db.setupDatabase()

    await inter.followup.send("Database is setup")

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
            if (isinstance(discordID, int)):
                print(discordID)
                try:
                    role = "whitelist"
                    player = pl.DiscordPlayer(discordID, steam64ID, role, name)
                    player.playerToDB()
                except (err.DuplicatePlayerPresent, err.PlayerNotFound, err.InvalidSteam64ID, err.InvalidRole) as error: 
                    print(error.message)

    await inter.followup.send("Spreadsheet has been imported")
    return

@bot.slash_command(description="prints the whitelist ID to console for easy setup of .env")
@commands.default_member_permissions(kick_members=True, manage_roles=True, administrator = True)
async def get_whitelist_id(inter):
    await inter.response.defer()
    for role in inter.author.roles:
        print (role, role.id)
    await inter.followup.send("done")
    return




#runs the actual bot, don't delete
bot.run(TOKEN)