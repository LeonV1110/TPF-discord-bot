import database_new as db
import helper as hlp
import os
import random
import whitelistDoc as wd
import errors as err
from dotenv import load_dotenv


load_dotenv()
WHITELISTROLE = int(os.getenv('WHITELIST_ROLE'))
# TODO, update to include all patreon roles after the rework

class Player:
    
    def playerToDB(self):
        self._checkDuplicateUser(self.steam64ID, self.discordID, self.TPFID)
        db.inputNewPlayer(self.TPFID, self.discordID, self.steam64ID, self.permission, self.name)
        return

    def updateWhitelist(self, orderID):
        db.updateWhiteList(self.TPFID, orderID) 
        return

    def updatePermission(self, role):
        permission = self._convertRoleToPermission(role)
        self.permission = permission
        db.updatePermission(self.TPFID, permission)
        wd.createWhitelistDoc() #TODO, change to a update whitelist doc function.
        return

    def deletePlayer(self):
        db.deletePlayer(TPFID=self.TPFID)
        return

    def _convertRoleToPermission(role):
        tier = ""
        if role == WHITELISTROLE: tier = "solo"
        #TODO, update to include all patreon roles after the rework
        return tier

    def _generateTPFID():
        TPFID = 0
        while db.checkTPFIDPressence(TPFID) or TPFID == 0:
            TPFID = random.randint(111111111111111, 999999999999999)
        return TPFID
    
    def _checkDuplicateUser(steam64ID, discordID, TPFID):
        if db.checkDiscordIDPressence(discordID):
            raise err.DuplicatePlayerPresent("This discordID is already in use")
        elif db.checkSteamIDPressence(steam64ID):
            raise err.DuplicatePlayerPresent("This steam64ID is already in use")
        elif db.checkTPFIDPressence(TPFID):
            raise err.DuplicatePlayerPresent("This TPFID is already in use")
        else:
            return

class newPlayer(Player):
    def __init__(self, discordID, steam64ID, role, name):
        permission = self._convertRoleToPermission(role)
        hlp.checkSteam64ID(steam64ID) #will raise InvalidSteam64ID exception
        self.steam64ID = steam64ID
        self.discordID = discordID
        self.permission = permission
        self.name = name
        self.TPFID = self._generateTPFID()
        return

class DatabasePlayer(Player):
    def __init__(self, discordID):
        player = db.getPlayer(discordID = discordID) #will raise PlayerNotFound exception
        self.steam64ID = player["Steam64ID"]
        self.discordID = player["DiscordID"]
        self.permission = player["Permission"]
        self.name = player["Name"]
        self.TPFID = player["TPFID"]
        self.whitelist = player["Whitelist"]
        return 