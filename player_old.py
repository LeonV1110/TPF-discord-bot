import database_old as db
import helper_old as hlp
import os
import random
import whitelistDoc as wd
import errors as err
from dotenv import load_dotenv


load_dotenv()

JUNIORADMINROLE = int(os.getenv('JUNIOR_ADMIN_ROLE'))
ADMINROLE = int(os.getenv('ADMIN_ROLE'))
SENIORADMINROLE = int(os.getenv('SENIOR_ADMIN_ROLE'))
DADMINROLE = int(os.getenv('DADMIN_ROLE'))
#CAMROLE = int(os.getenv('CAM_ROLE'))
#MVPROLE = int(os.getenv('MVP_ROLE'))
CREATORROLE = int(os.getenv('CREATOR_ROLE'))
WHITELISTROLE = int(os.getenv('WHITELIST_ROLE'))

class Player:
    def playerToDB(self):
        self._checkDuplicateUser(self.steam64ID, self.discordID, self.TPFID)
        db.inputNewPlayer(self.TPFID, self.discordID, self.steam64ID, self.permission, self.name)
        return

    def updateWhitelist(self, orderID):
        db.updateWhiteList(self.TPFID, orderID) 
        return

    def updatePermission(self, roles):
        permission = self._convertRoleToPermission(roles)
        check = ["none, whitelist"]
        if permission in check: return
        else:
            self.permission = permission
            db.updatePermission(self.TPFID, permission)
            wd.createWhitelistDoc() #TODO, change to a update whitelist doc function.
            return

    def deletePlayer(self):
        db.deletePlayer(TPFID=self.TPFID)
        return

    def _convertRoleToPermission(self, roles):
        roles.reverse()
        for role in roles:
            if role.id == DADMINROLE: return 'dadmin'
            elif role.id == SENIORADMINROLE: return 'senior'
            elif role.id == ADMINROLE: return 'admin'
            elif role.id == JUNIORADMINROLE: return 'junior'
            #elif role.id == CAMROLE: return 'cam'
            elif role.id == CREATORROLE: return 'creator'
            #elif role.id == MVPROLE: return 'MVP'
            elif role.id == WHITELISTROLE: return 'whitelist'
        return 'none'
    
    def _convertGroupToPermission(self, group):
        if group == 'whitelist': return 'none'
        elif group == 'mvp': return "MVP"
        elif group == 'creator': return "creator"
        elif group == 'caster': return 'cam' #TODO, may not be what we want
        return

    def _generateTPFID(self):
        TPFID = 0
        while db.checkTPFIDPressence(TPFID) or TPFID == 0:
            TPFID = random.randint(111111111111111, 999999999999999) #15 long ID
        return TPFID
    
    def _checkDuplicateUser(self, steam64ID, discordID, TPFID):
        if db.checkDiscordIDPressence(discordID):
            raise err.DuplicatePlayerPresent("This discordID is already in use")
        elif db.checkSteamIDPressence(steam64ID):
            raise err.DuplicatePlayerPresent("This steam64ID is already in use")
        elif db.checkTPFIDPressence(TPFID):
            raise err.DuplicatePlayerPresent("This TPFID is already in use")
        else:
            return

class SpreadsheetPlayer(Player):
    def __init__(self, discordID, steam64ID, group, name):
        hlp.checkSteam64ID(steam64ID) #will raise InvalidSteam64ID exception if invalid
        self.steam64ID = steam64ID
        self.discordID = discordID
        self.name = name
        self.TPFID = self._generateTPFID()
        permission = self._convertGroupToPermission(group)
        self.permission = permission
        return

class NewPlayer(Player):
    def __init__(self, discordID, steam64ID, role, name):
        permission = self._convertRoleToPermission(role)
        hlp.checkSteam64ID(steam64ID) #will raise InvalidSteam64ID exception if invalid
        self.steam64ID = steam64ID
        self.discordID = discordID
        self.permission = permission
        self.name = name
        self.TPFID = self._generateTPFID()
        return

class ListPlayer(Player):
    def __init__(self, playerList):
        self.steam64ID = playerList["Steam64ID"]
        self.discordID = playerList["DiscordID"]
        self.permission = playerList["Permission"]
        self.name = playerList["Name"]
        self.TPFID = playerList["TPFID"]
        self.whitelist = playerList["Whitelist"]
        return

class DatabasePlayer(ListPlayer):
    def __init__(self, discordID):
        player = db.getPlayer(discordID = discordID) #will raise PlayerNotFound exception
        super().__init__(player)
        return 

class SteamPlayer(ListPlayer):
    def __init__(self, steam64ID):
        player = db.getPlayer(steam64ID = steam64ID) #will raise PlayerNotFound exception
        super().__init__(player)
        return 
