import database as db
import errors as err
import player as pl
import os
from dotenv import load_dotenv
import random
import WhitelistOrder as wo

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


def updateWhitelist(member):
    discordID = member.id
    try:
        player = pl.DatabasePlayer(discordID)
    except err.PlayerNotFound as error:
        return error.message
    TPFID = player.TPFID
    try:
        order = wo.DatabaseOrder(TPFID)
        order.updateOrderTier(member.roles) # will deactivate the order if the tier is too low
    except err.OrderNotFound as error:
        return error.message
    return "You have received whitelist, thanks for suporting us!"