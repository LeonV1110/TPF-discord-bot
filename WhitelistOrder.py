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
        db.inputWhiteListOrder(self.orderID, self.TPFID, self.tier, self.active, self.whitelistees)
        return

    def updateTier(orderID, tier):
        db.updateTier(orderID, tier)
        return

    def updateOrderTier(self, role):
        tier = self._convertRoleToTier(role)
        self.tier = tier
        db.updateTier(self.orderID, tier)
        if not self._checkWhitelistees(): self.deactivateOrder()
        else: return

    #adds whitelist to the player in question
    def addPlayerToOrder(self, steam64ID):
        player = pl.SteamPlayer(steam64ID)
        TPFID = player.TPFID
        db.updateWhiteList(TPFID, self.orderID)
        db.updateWhitelistees(self.orderID, self.whitelistees+1)
        return

    def removePlayerFromOrder(self, steam64ID):
        player = pl.SteamPlayer(steam64ID)
        TPFID = player.TPFID
        db.updateWhiteList(TPFID, None) #may break, if so will need to make a seperate function to set whitelist value to "null" 
        db.updateWhitelistees(self.orderID, self.whitelistees-1)
        return
    
    def deactivateOrder(self):
        self.active = False
        db.updateActivity(self.orderID, False)
        return

    def reactivateOrder(self):
        self.active = True
        db.updateActivity(self.orderID, True)
        return

    #returns a list of player objects
    def getAllPlayersOnOrder(self):
        playersList = db.getAllPlayersOnOrder(self.orderID)
        resList = []
        for player in playersList:
            playerobj = pl.ListPlayer(player)
            resList.append(playerobj)
        return resList
    
    def deleteOrder(self):
        db.deleteWhitelistOrder(self.orderID)
        return

    def _generateOrderID(self):
        orderID = 0
        while orderID == 0 or db.checkOrderIDPressence(orderID):
            orderID = random.randint(1111111111111111, 9999999999999999) #16 long ID
        return orderID

    def _convertRoleToTier(self, role):
        if role == WHITELISTROLE: return 'solo'
        #elif role == #TODO tiers above solo whitelist, (after patreon rework)
        return

    def _checkDuplicateOrder(self, TPFID):
        if db.checkTPFIDPressenceInOrder(TPFID):
            raise err.DuplicateOrderPresent()
        return

    def _checkWhitelistees(self):
        if self.tier == 'solo' and self.whitelistees <= 1: return True
        #elif self.tier == "todo" and self.whitelistees <= "TODO": return True #template
        else: return False

class NewOrder(WhitelistOrder):
    def __init__(self, discordID, role):
        player = pl.DatabasePlayer(discordID)
        self.TPFID = player.TPFID
        self.tier = self._convertRoleToTier(role)
        orderID = self._generateOrderID()
        self.orderID = orderID
        self.activity = True
        self.whitelistees = 1
        self.whitelisted = 1 + len(self.getAllPlayersOnOrder(orderID))

class DatabaseOrder(WhitelistOrder):
    def __init__(self, TPFID):
        self.TPFID = TPFID
        order = db.getWhitelistOrder(TPFID)
        if order == (): raise err.OrderNotFound()
        self.tier = order["Tier"]
        orderID = order["OrderID"]
        self.orderID = orderID
        self.activity = order['Activity']
        self.whitelistees = order['Whitelistees']
        self.whitelisted = 1 + len(self.getAllPlayersOnOrder(orderID))