class DuplicatePlayerPresent(Exception):
    def __init__(self, message="there is already a player with your steam64 or discord ID"):
        self.message = message
        super().__init__(self.message)

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