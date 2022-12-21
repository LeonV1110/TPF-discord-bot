import database_new as db
import player_new as pl
import random
import os
import errors_new as err
from dotenv import load_dotenv


load_dotenv()
WHITELISTROLE = int(os.getenv('WHITELIST_ROLE'))
# TODO, update to include all patreon roles after the rework

class WhitelistOrder:

    def orderToDB(self):
        self._checkDuplicateOrder(self.TPFID)
        db.inputWhiteListOrder(self.orderID, self.TPFID, self.tier)
        return

    def updateTier(orderID, tier):
        db.updateTier(orderID, tier)
        return

    def updateOrder(self, role):
        tier = self._convertRoleToTier(role)
        self.tier = tier
        self.updateTier(self.orderID, tier)
        return

    #adds whitelist to the player in question
    def addPlayerToOrder(self, steam64ID):
        player = pl.SteamPlayer(steam64ID)
        TPFID = player.TPFID
        db.updateWhiteList(TPFID, self.orderID)
        return

    #returns a list of player objects
    def getAllPlayersOnOrder(orderID):
        playersList = db.getAllPlayersOnOrder(orderID)
        resList = []
        for player in playersList:
            playerobj = pl.ListPlayer(player)
            resList.append(playerobj)
        return resList
    
    def deleteOrder(self):
        db.deleteWhitelistOrder(self.orderID)
        return

    def _generateOrderID():
        orderID = 0
        while orderID == 0 or db.checkOrderIDPressence(orderID):
            orderID = random.randint(1111111111111111, 9999999999999999) #16 long ID
        return orderID

    def _convertRoleToTier(role):
        if role == WHITELISTROLE: return 'solo'
        #elif role == #TODO tiers above solo whitelist, (after patreon rework)
        return

    def _checkDuplicateOrder(TPFID):
        if db.checkTPFIDPressenceInOrder(TPFID):
            raise err.DuplicateOrderPresent()
        return

class NewOrder(WhitelistOrder):
    def __init__(self, discordID, role):
        player = pl.DatabasePlayer(discordID)
        self.TPFID = player.TPFID
        self.tier = self._convertRoleToTier(role)
        orderID = self._generateOrderID()
        self.orderID = orderID
        self.whitelisted = 1 + len(self.getAllPlayersOnOrder(orderID))

class DatabaseOrder(WhitelistOrder):
    def __init__(self, TPFID):
        self.TPFID = TPFID
        order = db.getWhitelistOrder(TPFID)
        self.tier = order["Tier"]
        orderID = order["OrderID"]
        self.orderID = orderID
        self.whitelisted = 1 + len(self.getAllPlayersOnOrder(orderID))