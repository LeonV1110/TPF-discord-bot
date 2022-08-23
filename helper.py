import database as db
import errors as err
import player as pl
import os
from dotenv import load_dotenv

load_dotenv()
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

def checkRole(role):
    valid = ["whitelist", "nothing"]
    if role in valid:
        return
    else:
        raise err.InvalidRole()

def checkDuplicateUser(steam64ID, discordID):
    if db.checkDiscordIDPressence(discordID):
        raise err.DuplicatePlayerPresent("This discordID is already in use")
    elif db.checkSteamIDPressence(steam64ID):
        raise err.DuplicatePlayerPresent("This steam64ID is already in use")
    else:
        return

def updateRoles(member):
    whitelist = updateWhitelist(member)
    return whitelist


def updateWhitelist(member):
    discordID = member.id
    try:
        player = pl.DatabasePlayer(discordID)
    except err.PlayerNotFound as error:
        return error.message
    
    discordRoles = member.roles
    res = "I wasn't able to find a whitelist role on your user, are you sure that you have connected your patreon to discord?"
    role = "nothing"
    for discordRole in discordRoles:
        if discordRole.id == WHITELISTROLE:
            role = "whitelist"
            res = "You have received whitelist, thanks for suporting us!"
    player.updateRole(role)

    return res