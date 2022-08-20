import database as db
import errors as err

def checkSteam64ID(steamID):
    
    #check if int
    try:
        int(steamID)
    except:
        return "A steam64ID contains just numbers."
    #check if not default steam64ID
    if (steamID == 76561197960287930):
        return "This is Gabe Newell's steam64ID, please make sure to enter yours."
    stringID = str(steamID)
    #check if first numbers match
    if (not stringID[0:7] == "7656119"):
        return "This is not a valid steam64ID."
    #check the length
    if (len(str(steamID)) < 17):
        return "This is not a valid steam64ID, as it is shorter."
    if (len(str(steamID)) > 17):
        return "This is not a valid steam64ID, as it is longer."
    
    return "suc6"

def checkDuplicateUser(steamID, disID):
    if db.checkSteamIDPressence(steamID):
        raise err.DuplicatePlayerPresent(steamID, disID)
    elif db.checkDiscordIDPressence(disID):
        raise err.DuplicatePlayerPresent(steamID, disID)
    else:
        return