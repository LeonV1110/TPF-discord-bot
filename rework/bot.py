import disnake
from disnake.ext import commands
from disnake import Interaction, Embed
from player import Player, NewPlayer, DatabasePlayer, SteamPlayer
import helper as hlp
import os
from dotenv import load_dotenv
from error import PlayerNotFound, InvalidSteam64ID, DuplicatePlayerPresent

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILDID = int(os.getenv('DISCORD_GUILD_ID'))

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True #TODO, probably not needed
bot = commands.Bot(intents = intents, command_prefix='/')

######################
###### events ########
######################

@bot.event
async def on_ready():
    print(f"We're logged in as {bot.user}")

@bot.event
async def on_member_update(before, after):
    pass #TODO

@bot.event
async def on_member_remove(member):
    pass #TODO

#########################################
########   Player Commands    ###########
#########################################

@bot.slash_command(discription = "Link your steam64ID with your discord account in our database") #Also actives whitelist and perms if role is present
async def register(inter, steam64id: str):
    await inter.response.defer(ephemeral=True)
    try:
        hlp.check_steam64ID(steam64id)
    except InvalidSteam64ID as error:
        await inter.followup.send(embed = Embed(title= error.message), ephemeral=True)
        return
    discordID = inter.author.id
    name = inter.author.name + "#" + inter.author.discriminator
    roles = inter.author.roles
    permission = hlp.convert_role_to_perm(roles)
    tier = hlp.convert_role_to_tier(roles)

    player = NewPlayer(steam64id, discordID, name, permission, tier)
    try:
        player.player_to_DB()
    except DuplicatePlayerPresent as error:
        await inter.followup.send(embed = Embed(title= error.message), ephemeral=True)
        return

    embed = Embed(title= 'Registrations was successful')
    await inter.followup.send(embed = embed, ephemeral=True)
    return

@bot.slash_command(discription = "Deletes your entry from our database, this will also remove your whitelist")
async def remove_myself_from_database(inter):
    await inter.response.defer(ephemeral=True)

    discordID = inter.author.id
    try:
        player = DatabasePlayer(discordID)
        player.delete_player()
    except PlayerNotFound as error:
        await inter.followup.send(embed = Embed(title= error.message), ephemeral=True)
        return

    embed = Embed(title='You have been successfully deleted from the database')
    await inter.followup.send(embed=embed, ephemeral=True)
    return

@bot.slash_command(discription = "Reloads your data in the database")
async def update_data(inter, steam64id: str):
    await inter.response.defer(ephemeral=True)

    try:
        hlp.check_steam64ID(steam64id)
    except InvalidSteam64ID as error:
        await inter.followup.send(embed = Embed(title= error.message), ephemeral=True)
        return
    
    discordID = inter.author.id
    name = inter.author.name + "#" + inter.author.discriminator
    roles = inter.author.roles
    permission = hlp.convert_role_to_perm(roles)
    tier = hlp.convert_role_to_tier(roles)

    try:
        player = DatabasePlayer(discordID)
        player.update(steam64id, discordID, name, permission, tier)
    except PlayerNotFound as error:
        await inter.followup.send(embed = Embed(title= error.message), ephemeral=True)
        return


    embed = Embed(title='Your data was successfully updated')
    await inter.followup.send(embed= embed, ephemeral=True)
    return

@bot.slash_command(discription = "TODO")
async def get_info(inter):
    await inter.response.defer(ephemeral=True)

    discordID = inter.author.id
    try:
        player = DatabasePlayer(discordID)
    except PlayerNotFound as error:
        await inter.followup.send(embed = Embed(title= error.message), ephemeral=True)
        return
    
    embed = Embed(title=player.name)
    embed.add_field(name = 'steam64 ID', value= player.steam64ID)
    embed.add_field(name = 'discord ID', value= player.discordID)
    embed.add_field(name = 'TPF ID', value= player.TPFID)

    await inter.followup.send(embed=embed, ephemeral=True)
    return

#########################################
########   Whitelist Commands    ########
#########################################

@bot.slash_command(discription = "TODO")
async def add_player_to_whitelist(inter, steam64id: str):
    pass #TODO

@bot.slash_command(discription = "TODO")
async def remove_player_from_whitelist(inter, steam64id: str):
    pass #TODO

@bot.slash_command(discription = "TODO")
async def update_player_on_whitelist(inter, old_steam64id: str, new_steam64id: str):
    pass #TODO

@bot.slash_command(discription = "TODO")
async def get_whitelist_info(inter):
    pass #TODO


#####################################
########   Admin Commands    ########
#####################################

@bot.slash_command(discription = "TODO")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def admin_nuke_player(inter, discordid: str, steam64id: str):
    pass #TODO

@bot.slash_command(discription = "TODO")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def admin_get_player_info(inter, discordid: str):
    pass #TODO

@bot.slash_command(discription = "TODO")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def admin_get_whitelist_info(inter, discordid: str):
    pass #TODO

#####################################
#########   Leon Commands    ########
#####################################

@bot.slash_command(discription = "TODO")
@commands.default_member_permissions(kick_members=True, manage_roles=True, administrator = True)
async def import_spreadsheet(inter):
    pass #TODO

@bot.slash_command(discription = "TODO")
@commands.default_member_permissions(kick_members=True, manage_roles=True, administrator = True)
async def setup_database(inter):
    pass #TODO

bot.run(TOKEN)