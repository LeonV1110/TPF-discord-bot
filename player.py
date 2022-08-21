import database as db
import whitelistDoc as wd

class Player:

    #initializes a player and uploads them to the database  
    def playerToDB(self):
        self.tpfID = db.inputNewPlayer(self.discordID, self.steam64ID, self.whitelist, self.name) #Does double duty, inputs player into the database and return the TPFID
    
    def updateWhitelist(self, whitelist):
        self.whitelist = whitelist
        db.updateWhitelist(self.whitelist, self.steam64ID, self.discordID)
        wd.createWhitelistDoc()
    
    def deletePlayerFromDB(self):
        db.deletePlayer(self.discordID)

class DiscordPlayer(Player):
    def __init__(self, discordID, steam64ID, whitelist, name):
            self.steam64ID = steam64ID
            self.discordID = discordID
            self.whitelist = whitelist
            self.name = name

class DatabasePlayer(Player):
    def __init__(self, discordID):
        player = db.getPlayerByDiscordID(discordID)
        self.steam64ID = player["Steam64ID"]
        self.discordID = player["DiscordID"]
        self.whitelist = player["Whitelist"]
        self.name = player["Name"]

