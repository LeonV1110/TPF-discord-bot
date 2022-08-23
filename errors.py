class DuplicatePlayerPresent(Exception):
    def __intit__(self, steam64ID, discordID, message = "there is already a player with your steam64 or discord ID"):
        self.steam64ID = steam64ID
        self.discordID = discordID
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return "Dis: " + str(self.discordID) + " Steam: " + str(self.steam64ID) + self.message

class PlayerNotFound(Exception):
    def __init__(self, message = "Player was not found"):
        self.message = message
        super().__init__(self.message)

class InvalidSteam64ID(Exception):
    def __init__(self, message = "This is not a valid steam64ID"):
        self.message = message
        super().__init__(self.message)

class InvalidRole(Exception):
    def __init__(self, message = "This is not a valid role"):
        self.message = message
        super().__init__(self.message)