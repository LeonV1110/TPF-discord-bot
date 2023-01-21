import os

import botHelper as bhlp
import disnake
import whitelistSpreadsheet
from disnake import Embed, Interaction
from disnake.ui import View, Button
from disnake.ext import commands
from dotenv import load_dotenv
from error import MyException
from pymysql import OperationalError
import buttonCallbacks as bcb

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
    try:
        bhlp.update_player_from_member(after)
    except MyException:
        #TODO, log these errors
        pass
    

@bot.event
async def on_member_remove(member):
    try:
        bhlp.update_player_from_member(member) #TODO, test if the member object is stripped of its roles when the player leaves
        # currently does not remove the whitelist or player entry, meaning a player can safely leave the discord if they're not the order owner
    except MyException:
        #TODO, log these errors
        pass

#########################################
########   Player Commands    ###########
#########################################

@bot.slash_command(description = "Link your steam64ID with your discord account in our database.") 
#Also actives whitelist and perms if role is present
async def register(inter, steam64id: str):
    await inter.response.defer(ephemeral=True)
    embed = Embed(title= 'Registrations was successful.')
    try:
        bhlp.register_player(member = inter.author, steam64ID = steam64id)
    except MyException as error:
        embed = Embed(title= error.message)
    except OperationalError:
        embed = Embed(title= "The bot is currently having issues, please try again later.")
    
    await inter.followup.send(embed = embed, ephemeral=True)
    return

    
@bot.slash_command(description = "Deletes your entry from our database, also removes your whitelist of anyone on your subscription.")
async def remove_myself_from_database(inter):
    await inter.response.defer(ephemeral=True)
    embed = Embed(title='You have been successfully deleted from the database.')

    try:
        bhlp.remove_player(member=inter.author)
    except MyException as error:
        embed = Embed(title= error.message)
    except OperationalError:
        embed = Embed(title= "The bot is currently having issues, please try again later.")

    await inter.followup.send(embed=embed, ephemeral=True)
    return

@bot.slash_command(description = "Reloads your data in the database.")
async def update_data(inter):
    await inter.response.defer(ephemeral=True)
    embed = Embed(title='Your data was successfully updated.')

    try:
        bhlp.update_player_from_member(member=inter.author)
    except MyException as error:
        embed = Embed(title= error.message)
    except OperationalError:
        embed = Embed(title= "The bot is currently having issues, please try again later.")

    await inter.followup.send(embed= embed, ephemeral=True)
    return

@bot.slash_command(description= "Changes your steam64ID in the database.")
async def change_steam64id(inter, steam64id):
    await inter.response.defer(ephemeral=True)
    embed = Embed(title='Your steam64id was successfully updated.')

    try:
        bhlp.change_steam64ID(inter.author, steam64id)
    except MyException as error:
        embed = Embed(title= error.message)
    except OperationalError:
        embed = Embed(title= "The bot is currently having issues, please try again later.")

    await inter.followup.send(embed= embed, ephemeral=True)
    return

@bot.slash_command(description = "See what information we have about you in the database.")
async def get_info(inter):
    await inter.response.defer(ephemeral=True)

    try:
        embed = bhlp.get_player_info(member = inter.author)
    except MyException as error:
        embed = Embed(title= error.message)
    except OperationalError:
        embed = Embed(title= "The bot is currently having issues, please try again later.")

    await inter.followup.send(embed= embed, ephemeral=True)
    return

#########################################
########   Whitelist Commands    ########
#########################################

@bot.slash_command(description = "Adds a player to your whitelist subscription. Use their Steam64ID.")
async def add_player_to_whitelist(inter, steam64id: str):
    await inter.response.defer(ephemeral=True)
    
    try:
        embed = bhlp.add_player_to_whitelist(owner_member=inter.author, player_steam64ID=steam64id)
    except MyException as error:
        embed = Embed(title= error.message)
    except OperationalError:
        embed = Embed(title= "The bot is currently having issues, please try again later.")  

    await inter.followup.send(embed = embed, ephemeral=True)
    return

@bot.slash_command(description = "Removes a player from your whitelist subscription. Use their steam64ID.")
async def remove_player_from_whitelist(inter, steam64id: str):
    await inter.response.defer(ephemeral=True)

    try:
        embed = bhlp.remove_player_from_whitelist(owner_member=inter.author, player_steam64ID=steam64id)
    except MyException as error:
        embed = Embed(title= error.message)
    except OperationalError:
        embed = Embed(title= "The bot is currently having issues, please try again later.")  

    await inter.followup.send(embed = embed, ephemeral=True)
    return

@bot.slash_command(description = "Replaces one player for another on your subscription. First steam64ID is replaced with the 2nd one.")
async def update_player_on_whitelist(inter, old_steam64id: str, new_steam64id: str):
    await inter.response.defer(ephemeral=True)

    try: 
        embed = bhlp.update_player_on_whitelist(owner_member=inter.author, old_player_steam64ID=old_steam64id, new_player_steam64ID=new_steam64id)
    except MyException as error:
        embed = Embed(title= error.message)
    except OperationalError:
        embed = Embed(title= "The bot is currently having issues, please try again later.")

    await inter.followup.send(embed = embed, ephemeral=True)
    return

@bot.slash_command(description = "See the current state of your whitelist subscription in our database.")
async def get_whitelist_subscription_info(inter):
    await inter.response.defer(ephemeral=True)
    
    try:
        embed = bhlp.get_whitelist_info(member=inter.author)
    except MyException as error:
        embed = Embed(title= error.message)
    except OperationalError:
        embed = Embed(title= "The bot is currently having issues, please try again later.")
    
    await inter.followup.send(embed = embed, ephemeral=True)
    return
    

#####################################
########   Admin Commands    ########
#####################################

@bot.slash_command(description = "Removes a player from the database, including thier whitelist order and whitelists on that order.")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def admin_nuke_player(inter, discordid: str, steam64id: str):
    await inter.response.defer(ephemeral=True)

    try:
        p1 = bhlp.get_player(discordID = discordid)
        p2 = bhlp.get_player(steam64ID = steam64id)
        if p1 == p2:
            bhlp.remove_player(discordid)
            embed = Embed(title=p1.name + ' has been successfully deleted from the database.')
        else:
            embed = Embed(title="The discordID and steam64ID don't match, double check and try again. If the issue persists you can annoy Leon I guess...")
    except MyException as error:
        embed = Embed(title= error.message)
    except OperationalError:
        embed = Embed(title= "The bot is currently having issues, please try again later.")

    await inter.followup.send(embed = embed, ephemeral=True)
    return

@bot.slash_command(description = "Get player info on player.")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def admin_get_player_info(inter, discordid: str):
    await inter.response.defer()
    try:
        embed = bhlp.get_player_info(discordID=discordid)
    except MyException as error:
        embed = Embed(title= error.message)
    except OperationalError:
        embed = Embed(title= "The bot is currently having issues, please try again later.")
    
    await inter.followup.send(embed=embed)
    return

@bot.slash_command(description = "Get whitelist info on players whitelist subscription")
@commands.default_member_permissions(kick_members=True, manage_roles=True)
async def admin_get_whitelist_info(inter, discordid: str):
    await inter.response.defer()
    
    try:
        embed = bhlp.get_whitelist_info(discordID= discordid)
    except MyException as error:
        embed = Embed(title= error.message)
    except OperationalError:
        embed = Embed(title= "The bot is currently having issues, please try again later.")

    await inter.followup.send(embed=embed)
    return

#####################################
#########   Leon Commands    ########
#####################################

@bot.slash_command(description = "Imports whitelist from the spreadsheet, don't touch unless you're called Leon")
@commands.default_member_permissions(kick_members=True, manage_roles=True, administrator = True)
async def import_spreadsheet(inter):
    await inter.response.defer(ephemeral=True)
    embed = Embed(title = 'Done!')

    try:
        whitelistSpreadsheet.import_spreadsheet(bot)
    except MyException as error:
        embed = Embed(title= error.message)
    except OperationalError:
        embed = Embed(title= "The bot is currently having issues, please try again later.")
    
    await inter.followup.send(embed = embed, ephemeral=True)
    return

@bot.slash_command(description = "Does the database setup, don't touch unless you're called Leon.")
@commands.default_member_permissions(kick_members=True, manage_roles=True, administrator = True)
async def setup_database(inter):
    await inter.response.defer()
    try: 
        setup_database()
    except:
        await inter.followup.send(embed = Embed(title= 'I have made a booboo, please go fix it.'))
        return
    embed = Embed(title = 'Done')
    await inter.followup.send(embed = embed)
    return

@bot.slash_command(description = "dont worry")
@commands.default_member_permissions(kick_members=True, manage_roles=True, administrator = True)
async def get_role_ids(inter):
    await inter.response.defer()
    roles = inter.author.roles
    for role in roles:
        print(role)
        print(role.id)
    await inter.followup.send(embed = Embed(title= "Boo"))
    return


@bot.slash_command(description = "Dont worry, don't touch unless you're called Leon.")
@commands.default_member_permissions(kick_members=True, manage_roles=True, administrator = True)
async def testing(inter):
    await inter.response.defer()
    embed = Embed(title= "Boo", colour = disnake.Colour.gold(), description="aardappels")
    embed.set_footer(text = "idk")

    view = disnake.ui.View()
    view.add_item(disnake.ui.Button(label='test'))
    await inter.followup.send(embed = embed, view= view)
    return

@bot.slash_command(description = "Dont worry, don't touch unless you're called Leon.")
@commands.default_member_permissions(kick_members=True, manage_roles=True, administrator = True)
async def explain_embed(inter):
    await inter.response.defer()
    embed = Embed(title= 'The TPF whitelist bot', colour= disnake.Colour.dark_gold())#TODO fix colour
    embed.add_field(name = '/register', value = '''
        Register yourself in the database by using this command, in this command you wil have to input your Steam64 ID. Hit enter when you are done and wait for the bot to complete the procces. \n
	    - To find your Steam64 ID go to the settings page on your steam account and click on the "View Account Details" option. A new page will open in steam, at the top it will state "Steam64 ID: 7656119xxxxxxxxxx" (with the x's being unique to your account). This is your steam64ID that you need to use when registering.
        ''', inline= False)
    embed.add_field(name = '/remove_myself_from_database', value = '''
        If for whatever reason you want to remove yourself from the database you can use this command. \n
        -NOTE: this means that you and the potential other players on your whitelist will no longer be whitelisted on our servers!
        ''', inline= False)
    embed.add_field(name = '/change_steam64id', value = '''
        To change your Steam64 ID use this command and enter your (new) Steam64 ID.
        ''', inline= False)
    embed.add_field(name = '/get_info', value = '''
        Use this command or press the button below to check if you are whitelisted.\n
        - If you notice that the Steam64 ID you provided is wrong use the command /change_steam64id
        - If the "whitelist status" shows "Active" you are sucessfully whitelisted, thank you for your contribution!
        - If the "whitelist status" shows "Inactive" you likely do not have the whitelist role, try reconnecting your patreon to discord and confirm your patreon subscription.
        ''', inline= False)
    embed.add_field(name = '/update_data', value = '''
        If the database has not recognized your (Discord) Whitelist role yet, use this command or the button below to force it to update.
        ''', inline= False)
    embed.add_field(name = '/add_player_to_whitelist', value = '''
        This command is used to add a player to your whitelist subscription, do make sure that you have a whitelist of a sufficient tier.
        This command will ask you to provide a Steam64 ID from those that you want to add. Make sure that they give you the Steam64 ID that they used to register with.
        ''', inline= False)
    embed.add_field(name = '/remove_player_from_whitelist', value = '''
        This command will remove players from your whitelist subscription. 
        This command will ask you to provide a Steam64 ID from those that you want to remove. Make sure you got the correct one by using the command /get_whitelist_subscription_info.
        ''', inline= False)
    embed.add_field(name = '/update_player_from_whitelist', value = '''
        This command will replace one player for another on your whitelist subscription. 
        First provide the Steam64 ID you want to replace, then provide the Steam64 ID you want to add.
        ''', inline= False)
    embed.add_field(name = '/get_whitelist_subscription_info', value = '''
        Use this command or press the button below to check who is on your whitelist subscription and if it's active or not.
        ''', inline= False)

    
    get_info_button = Button(label= 'Get My Info')
    get_info_button.callback = bcb.get_info_button_callback

    update_data_button = Button(label='Update My Data')
    update_data_button.callback = bcb.update_data_button_callback

    get_whitelist_info_button = Button(label= 'Get My Whitelist Info')
    get_whitelist_info_button.callback = bcb.get_whitelist_info_button_callback

    view = View()
    view.add_item(get_info_button)
    view.add_item(update_data_button)
    view.add_item(get_whitelist_info_button)

    await inter.followup.send(embed = embed, view= view)
    return

bot.run(TOKEN)