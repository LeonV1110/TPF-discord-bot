from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILDID = int(os.getenv('DISCORD_GUILD_ID'))
WHITELISTROLE = os.getenv('WHITELIST_ROLE')

def connectDatabase():
    do = "something"
    #TODO

def addWhitelist():
    do = "something"
    print("Add whitelist started")
    #TODO