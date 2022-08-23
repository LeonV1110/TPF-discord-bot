import databaseNew as db
import helperNew as hlp

class Player:
    
    def playerToDB(self):
        hlp.checkDuplicateUser(self.steam64ID, self.discordID)
        self.playerID = db.inputNewPlayer(self.discordID, self.steam64ID, self.role, self.name) #Does double duty, inputs player into the database and return the TPFID
        return

    def updateRole(self, role):
        hlp.checkRole(role)
        self.role = role
        db.updateRole(role, self.discordID)
        return

    def deletePlayer(self):
        db.deletePlayer(discordID=self.discordID)
        return

class DiscordPlayer(Player):
    def __init__(self, discordID, steam64ID, role, name):
        hlp.checkSteam64ID(steam64ID) #will raise InvalidSteam64ID exception
        hlp.checkRole(role) # will raise InvalidRole exception
        self.steam64ID = steam64ID
        self.discordID = discordID
        self.role = role
        self.name = name
        return

class DatabasePlayer(Player):
    def __init__(self, discordID):
        player = db.getPlayerByDiscordID(discordID) #will raise PlayerNotFound exception
        self.steam64ID = player["steam64ID"]
        self.discordID = player["discordID"]
        self.role = player["role"]
        self.name = player["name"]
        self.playerID = player["playerID"]
        return