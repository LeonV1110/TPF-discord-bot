import database as db

class Player:

    #initializes a player and uploads them to the database  
    def playerToDB(self):
        self.tpfID = db.inputNewPlayer(self.discordID, self.steam64ID, self.whitelist) #Does double duty, inputs player into the database and return the TPFID
        


    def updateWhitelist(self, whitelist):
        self.whitelist = whitelist
        db.updateWhitelist(self.whitelist, self.steam64ID, self.discordID)

class DiscordPlayer(Player):
    def __init__(self, discordID, steam64ID, whitelist):
            self.steam64ID = steam64ID
            self.discordID = discordID
            self.whitelist = whitelist

class DatabasePlayer(Player):
    def __init__(self, discordID):
        player = db.getPlayerByDiscordID(discordID)
        self.steam64ID = player["Steam64ID"]
        self.discordID = player["DiscordID"]
        self.whitelist = player["Whitelist"]

