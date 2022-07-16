from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILDID = int(os.getenv('DISCORD_GUILD_ID'))
WHITELISTROLE = os.getenv('WHITELIST_ROLE')

def connectDatabase():
    return
    #TODO

def addWhitelist():
    print("Add whitelist started")
    return
    #TODO

def getWhitelistStatus(id):
    #TODO
    
    return True