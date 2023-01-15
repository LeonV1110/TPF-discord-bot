class PlayerNotFound(Exception):
    def __init__(self, message = "Player was not found"):
        self.message = message
        super().__init__(self.message)

class DuplicatePlayerPresent(Exception):
    def __init__(self, message="There is already a player with your steam64 or discord ID"):
        self.message = message
        super().__init__(self.message)

class InvalidSteam64ID(Exception):
    def __init__(self, message = "This is not a valid steam64ID"):
        self.message = message
        super().__init__(self.message)

class InvalidDiscordID(Exception):
    def __init__(self, message = "This is not a valid discordID"):
        self.message = message
        super().__init__(self.message)

class InsuffientTier(Exception):
    def __init__(self, message = "Your whitelist tier is insuffient for the current amount of whitelists"):
        self.message = message
        super().__init__(self.message)

class WhitelistNotFound(Exception):
    def __init__(self, message = "This player does not have a whitelist on your subscription"):
        self.message = message
        super().__init__(self.message)