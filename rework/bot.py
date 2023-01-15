import disnake
from disnake.ext import commands
from disnake import Interaction, Embed
from player import Player, NewPlayer, DatabasePlayer, SteamPlayer, TPFIDPlayer
import helper as hlp
import os
from dotenv import load_dotenv
from error import PlayerNotFound, InvalidSteam64ID, InvalidDiscordID, DuplicatePlayerPresent, InsuffientTier, WhitelistNotFound
from pymysql import OperationalError

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
    discordID = after.id
    try:
        player = DatabasePlayer(discordID)
        roles = after.roles
        tier = hlp.convert_role_to_tier(roles)
        permission = hlp.convert_role_to_perm(roles)
        name = after.name + "#" + after.discriminator
        player.update(player.steam64ID, discordID, name, permission, tier)
    except (PlayerNotFound, OperationalError):
        #TODO, log these errors
        pass
    

@bot.event
async def on_member_remove(member):
    discordID = member.id
    try:
        player = DatabasePlayer(discordID)
        tier = None
        player.update_whitelist_order(tier)
        # currently does not remove the whitelist or player entry, meaning a player can safely leave the discord if they're not the order owner
    except (PlayerNotFound, OperationalError):
        #TODO, log these errors
        pass

#########################################
########   Player Commands    ###########
#########################################

@bot.slash_command(discription = "Link your steam64ID with your discord account in our database") 
#Also actives whitelist and perms if role is present
async def register(inter, steam64id: str):
    await inter.response.defer(ephemeral=True)
    try:
        hlp.check_steam64ID(steam64id)
    except InvalidSteam64ID as error:
        await inter.followup.send(embed = Embed(title= error.message), ephemeral=True)
        return

    discordID = str(inter.author.id)
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
    except OperationalError:
        await inter.followup.send(embed = Embed(title= "the bot is currently having issues, please try again later."), ephemeral=True)
        return

    embed = Embed(title= 'Registrations was successful')
    await inter.followup.send(embed = embed, ephemeral=True)
    return

@bot.slash_command(discription = "Deletes your entry from our database, this will also remove your whitelist and the whitelists of anyone on your subscription.")
async def remove_myself_from_database(inter):
    await inter.response.defer(ephemeral=True)

    discordID = str(inter.author.id)
    try:
        player = DatabasePlayer(discordID)
        player.delete_player()
    except PlayerNotFound as error:
        await inter.followup.send(embed = Embed(title= error.message), ephemeral=True)
        return
    except OperationalError:
        await inter.followup.send(embed = Embed(title= "the bot is currently having issues, please try again later."), ephemeral=True)
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
    except OperationalError:
        await inter.followup.send(embed = Embed(title= "the bot is currently having issues, please try again later"), ephemeral=True)
        return

    embed = Embed(title='Your data was successfully updated')
    await inter.followup.send(embed= embed, ephemeral=True)
    return

@bot.slash_command(discription = "See what information we have about you in the database")
async def get_info(inter):
    await inter.response.defer(ephemeral=True)

    discordID = str(inter.author.id)
    try:
        player = DatabasePlayer(discordID)
    except PlayerNotFound as error:
        await inter.followup.send(embed = Embed(title= error.message), ephemeral=True)
        return
    except OperationalError:
        await inter.followup.send(embed = Embed(title= "the bot is currently having issues, please try again later"), ephemeral=True)
        return
    
    embed = Embed(title=player.name)
    embed.add_field(name = 'steam64 ID', value= player.steam64ID)
    embed.add_field(name = 'discord ID', value= player.discordID)
    embed.add_field(name = 'TPF ID', value= player.TPFID)
    
    if player.check_whitelist():
        whitelist_status = 'Active'
    else:
        whitelist_status = 'Inactive'
    embed.add_field(name = 'Whitelist Status', value = whitelist_status)
    if player.whitelist_order is not None:
        embed.add_field(name = 'Whitelist Subscription', value= player.whitelist_order.tier)

    await inter.followup.send(embed=embed, ephemeral=True)
    return

#########################################
########   Whitelist Commands    ########
#########################################

@bot.slash_command(discription = "Adds a player to your whitelist subscription. They have to be registered and you need to fill in thier Steam64ID")
async def add_player_to_whitelist(inter, steam64id: str):
    await inter.response.defer(ephemeral=True)
    try:
        hlp.check_steam64ID(steam64id)
    except InvalidSteam64ID as error:
        await inter.followup.send(embed = Embed(title= error.message), ephemeral=True)
        return

    discordID = str(inter.author.id)
    try: 
        owner = DatabasePlayer(discordID)
        player = SteamPlayer(steam64id)
        if owner.whitelist_order is None:
            await inter.followup.send(embed = Embed(title = "It seems like you don't have a whitelist subscription. Make sure you are subscribed on Patreon and reconnect your discord account to Patreon"), ephemeral = True)
            return
        else:
            owner.whitelist_order.add_whitelist(player.TPFID)
    except (InsuffientTier, PlayerNotFound) as error:
        await inter.followup.send(embed = Embed(title = error.message), ephemeral = True)
        return
    except OperationalError:
        await inter.followup.send(embed = Embed(title= "the bot is currently having issues, please try again later"), ephemeral=True)
        return

    embed = Embed(title= player.name + ' has been successfully added to your subscription')
    await inter.followup.send(embed = embed, ephemeral=True)
    return

@bot.slash_command(discription = "Removes a player from your whitelist subscription. Use their steam64ID.")
async def remove_player_from_whitelist(inter, steam64id: str):
    await inter.response.defer(ephemeral=True)
    try:
        hlp.check_steam64ID(steam64id)
    except InvalidSteam64ID as error:
        await inter.followup.send(embed = Embed(title= error.message), ephemeral=True)
        return
    discordID = str(inter.autho.id)
    try: 
        owner = DatabasePlayer(discordID)
        player = SteamPlayer(steam64id)
        owner.whitelist_order.remove_whitelist(player.TPFID)
    except (InsuffientTier, PlayerNotFound, WhitelistNotFound) as error:
        await inter.followup.send(embed = Embed(title = error.message), ephemeral = True)
        return
    except OperationalError:
        await inter.followup.send(embed = Embed(title= "the bot is currently having issues, please try again later"), ephemeral=True)
        return
    embed = Embed(title = player.name + ' has been successfully removed from your subscription')
    await inter.followup.send(embed = embed, ephemeral=True)
    return

@bot.slash_command(discription = "Replaces one player for another on your whitelist subscription. First fill in the steam64Id of who you want to replace, then fill in the steam64ID of who you want to add instead.")
async def update_player_on_whitelist(inter, old_steam64id: str, new_steam64id: str):
    await inter.response.defer(ephemeral=True)
    try:
        hlp.check_steam64ID(old_steam64id)
        hlp.check_steam64ID(new_steam64id)
    except InvalidSteam64ID as error:
        await inter.followup.send(embed = Embed(title= error.message), ephemeral=True)
        return
    discordID = str(inter.autho.id)
    try: 
        owner = DatabasePlayer(discordID)
        old_player = SteamPlayer(old_steam64id)
        new_player = SteamPlayer(new_steam64id)
        owner.whitelist_order.remove_whitelist(old_player.TPFID)
        owner.whitelist_order.add_whitelist(new_player.TPFID)
    except (InsuffientTier, PlayerNotFound, WhitelistNotFound) as error:
        await inter.followup.send(embed = Embed(title = error.message), ephemeral = True)
        return
    except OperationalError:
        await inter.followup.send(embed = Embed(title= "the bot is currently having issues, please try again later"), ephemeral=True)
        return
    embed = Embed(title = old_player.name + ' has been successfully replaces with' + new_player.name + '.')
    await inter.followup.send(embed = embed, ephemeral=True)
    return

@bot.slash_command(discription = "See the current state of your whitelist subscription in our database")
async def get_whitelist_subscription_info(inter):
    await inter.response.defer(ephemeral=True)
    discordID = str(inter.author.id)
    try:
        owner = DatabasePlayer(discordID)
        if owner.whitelist_order is None:
            await inter.followup.send(embed = Embed(title= "You have no whitelist subscription, /get_info instead"), ephemeral=True)
            return
        else:
            whitelist_order = owner.whitelist_order
            whitelistees = []
            for whitelist in whitelist_order.whitelists:
                TPFID = whitelist.TPFID
                try: 
                    player = TPFIDPlayer(TPFID)
                    whitelistees.append(player.name)

                except (InsuffientTier, PlayerNotFound, WhitelistNotFound) as error:
                    await inter.followup.send(embed = Embed(title = error.message), ephemeral = True)
                    return
                except OperationalError:
                    await inter.followup.send(embed = Embed(title= "the bot is currently having issues, please try again later"), ephemeral=True)
                    return
            if owner.check_whitelist():
                whitelist_status = 'Active'
            else:
                whitelist_status = 'Inactive'
            embed = Embed(title = 'Whitelist Subscription: ' + owner.name)
            embed.add_field(name = 'Tier: ', value= whitelist_order.tier)
            embed.add_field(name = 'Status: ', value = whitelist_status)
            embed.add_field(name = 'Whitelists: ', value= whitelistees)

            await inter.followup.send(embed = embed, ephemeral=True)
            return
    except PlayerNotFound as error:
        await inter.followup.send(embed = Embed(title= error.message), ephemeral=True)
        return
    except OperationalError:
        await inter.followup.send(embed = Embed(title= "the bot is currently having issues, please try again later"), ephemeral=True)
        return
    



#####################################
########   Admin Commands    ########
#####################################

@bot.slash_command(discription = "Removes a player from the database, including thier whitelist order and whitelists on that order.")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def admin_nuke_player(inter, discordid: str, steam64id: str):
    await inter.response.defer(ephemeral=True)
    try:
        hlp.check_discordID(discordid)
        hlp.check_steam64ID(steam64id)
    except (InvalidSteam64ID, InvalidDiscordID) as error:
        await inter.followup.send(embed = Embed(title = error.message), ephemeral = True)
        return
    
    try:
        player = DatabasePlayer(discordid)
        if player.steam64ID == steam64id:
            player.delete_player()
        else:
            await inter.followup.send(embed = Embed(title = 'The steam64ID does not match with the discordID, thus the player was not deleted. ', ephemeral = True))
            return
    except (PlayerNotFound) as error:
        await inter.followup.send(embed = Embed(title = error.message), ephemeral = True)
        return
    except OperationalError:
        await inter.followup.send(embed = Embed(title= "the bot is currently having issues, please try again later"), ephemeral=True)
        return

    embed = Embed(title = player.name + ' has been successfully deleted from the database.')
    await inter.followup.send(embed = embed, ephemeral=True)
    return

@bot.slash_command(discription = "Get player info on player")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def admin_get_player_info(inter, discordid: str):
    await inter.response.defer()
    try:
        hlp.check_discordID(discordid)
    except InvalidDiscordID as error:
        await inter.followup.send(embed = Embed(title= error.message))
        return

    discordID = discordid
    try:
        player = DatabasePlayer(discordID)
    except PlayerNotFound as error:
        await inter.followup.send(embed = Embed(title= error.message))
        return
    except OperationalError:
        await inter.followup.send(embed = Embed(title= "the bot is currently having issues, please try again later"))
        return
    
    embed = Embed(title=player.name)
    embed.add_field(name = 'steam64 ID', value= player.steam64ID)
    embed.add_field(name = 'discord ID', value= player.discordID)
    embed.add_field(name = 'TPF ID', value= player.TPFID)
    
    if player.check_whitelist():
        whitelist_status = 'Active'
    else:
        whitelist_status = 'Inactive'
    embed.add_field(name = 'Whitelist Status', value = whitelist_status)
    if player.whitelist_order is not None:
        embed.add_field(name = 'Whitelist Subscription', value= player.whitelist_order.tier)

    await inter.followup.send(embed=embed)
    return

@bot.slash_command(discription = "Get whitelist info on players whitelist subscription")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def admin_get_whitelist_info(inter, discordid: str):
    await inter.response.defer()
    try:
        hlp.check_discordID(discordid)
    except InvalidDiscordID as error:
        await inter.followup.send(embed = Embed(title= error.message))
        return

    discordID = discordid
    try:
        owner = DatabasePlayer(discordID)
        if owner.whitelist_order is None:
            await inter.followup.send(embed = Embed(title= "You have no whitelist subscription, /get_info instead"))
            return
        else:
            whitelist_order = owner.whitelist_order
            whitelistees = []
            for whitelist in whitelist_order.whitelists:
                TPFID = whitelist.TPFID
                try: 
                    player = TPFIDPlayer(TPFID)
                    whitelistees.append(player.name)

                except (InsuffientTier, PlayerNotFound, WhitelistNotFound) as error:
                    await inter.followup.send(embed = Embed(title = error.message))
                    return
                except OperationalError:
                    await inter.followup.send(embed = Embed(title= "the bot is currently having issues, please try again later"))
                    return
            if owner.check_whitelist():
                whitelist_status = 'Active'
            else:
                whitelist_status = 'Inactive'
            embed = Embed(title = 'Whitelist Subscription: ' + owner.name)
            embed.add_field(name = 'Tier: ', value= whitelist_order.tier)
            embed.add_field(name = 'Status: ', value = whitelist_status)
            embed.add_field(name = 'Whitelists: ', value= whitelistees)

            await inter.followup.send(embed = embed)
            return
    except PlayerNotFound as error:
        await inter.followup.send(embed = Embed(title= error.message))
        return
    except OperationalError:
        await inter.followup.send(embed = Embed(title= "the bot is currently having issues, please try again later"))
        return

#####################################
#########   Leon Commands    ########
#####################################

@bot.slash_command(discription = "Imports whitelist from the spreadsheet, don't touch unless you're caleed Leon")
@commands.default_member_permissions(kick_members=True, manage_roles=True, administrator = True)
async def import_spreadsheet(inter):
    await inter.response.defer(ephemeral=True)
    #TODO
    embed = Embed(title = '')
    await inter.followup.send(embed = embed, ephemeral=True)
    return

@bot.slash_command(discription = "Does the database setup, don't touch unless you're called Leon")
@commands.default_member_permissions(kick_members=True, manage_roles=True, administrator = True)
async def setup_database(inter):
    await inter.response.defer()
    try: 
        setup_database()
    except:
        await inter.followup.send(embed = Embed(title= 'I have made a booboo, please go fix it'))
        return
    embed = Embed(title = 'Done')
    await inter.followup.send(embed = embed)
    return

@bot.slash_command(discription = "dont worry")
@commands.default_member_permissions(kick_members=True, manage_roles=True, administrator = True)
async def get_role_ids(inter):
    await inter.response.defer()
    roles = inter.author.roles
    for role in roles:
        print(role)
        print(role.id)
    await inter.followup.send(embed = Embed(title= "Boo"))
    return

bot.run(TOKEN)