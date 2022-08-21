import database as db
import errors as err
import player as pl
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILDID = int(os.getenv('DISCORD_GUILD_ID'))
WHITELISTROLE = int(os.getenv('WHITELIST_ROLE'))

def checkSteam64ID(steamID):
    #check if int
    try:
        int(steamID)
    except:
        raise err.InvalidSteam64ID("A steam64ID contains just numbers.")
    stringID = str(steamID)
    #check if not default steam64ID
    if (stringID == str(76561197960287930)):
        raise err.InvalidSteam64ID("This is Gabe Newell's steam64ID, please make sure to enter yours.")
    #check if first numbers match
    if (not stringID[0:7] == "7656119"):
       raise err.InvalidSteam64ID("This is not a valid steam64ID.")
    #check the length
    if (len(str(steamID)) < 17):
       raise err.InvalidSteam64ID("This is not a valid steam64ID, as it is shorter than 17 characters.")
    if (len(str(steamID)) > 17):
        raise err.InvalidSteam64ID("This is not a valid steam64ID, as it is longer than 17 characters.")
    return


def checkDuplicateUser(steamID, disID):
    if db.checkSteamIDPressence(steamID):
        raise err.DuplicatePlayerPresent(steamID, disID)
    elif db.checkDiscordIDPressence(disID):
        raise err.DuplicatePlayerPresent(steamID, disID)
    else:
        return

def updateWhitelist(member):
    discordID = member.id
    try:
        player = pl.DatabasePlayer(discordID)
    except err.PlayerNotFound:
        return "You are not in our database, please register instead"
    
    roles = member.roles
    res = "I wasn't able to find a whitelist role on your user, are you sure that you have connected your patreon to discord?"
    whitelist = False
    for role in roles:
        if role.id == WHITELISTROLE:
            whitelist = True
            res = "You have received whitelist, thanks for suporting us!"
    player.updateWhitelist(whitelist)
    
    return res