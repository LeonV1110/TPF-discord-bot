import database as db
import whitelistDoc as wd
import helper as hlp

class Player:

    #initializes a player and uploads them to the database  
    def playerToDB(self):
        hlp.checkDuplicateUser(self.steam64ID, self.discordID)
        self.tpfID = db.inputNewPlayer(self.discordID, self.steam64ID, self.whitelist, self.name) #Does double duty, inputs player into the database and return the TPFID
    
    def updateWhitelist(self, whitelist):
        self.whitelist = whitelist
        db.updateWhitelist(self.whitelist, self.steam64ID, self.discordID)
        wd.createWhitelistDoc()
    
    def deletePlayerFromDB(self):
        db.deletePlayer(self.discordID)

class DiscordPlayer(Player):
    def __init__(self, discordID, steam64ID, whitelist, name):
            hlp.checkSteam64ID(steam64ID) #will throw InvalidSteam64ID error
            self.steam64ID = steam64ID
            self.discordID = discordID
            self.whitelist = whitelist
            self.name = name

class DatabasePlayer(Player):
    def __init__(self, discordID):
        player = db.getPlayerByDiscordID(discordID) #will throw PlayerNotFound error
        self.steam64ID = player["Steam64ID"]
        self.discordID = player["DiscordID"]
        self.whitelist = player["Whitelist"]
        self.name = player["Name"]

