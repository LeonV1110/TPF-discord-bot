from dotenv import load_dotenv
import os
import pymysql as mySQL

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILDID = int(os.getenv('DISCORD_GUILD_ID'))
WHITELISTROLE = os.getenv('WHITELIST_ROLE')
DATABASEUSER = os.getenv('DATABASE_USERNAME')
DATABASEPSW = os.getenv('DATABASE_PASSWORD')

def connectDatabase():
    connection = mySQL.connect(host='localhost', user = DATABASEUSER, password= DATABASEPSW, charset='utf8mb4', cursorclass=mySQL.cursors.DictCursor, database='tpf')
    return connection
    #TODO

def addWhitelist():
    print("Add whitelist started")
    return
    #TODO

def getWhitelistStatus(discordId, TPFID):
    connection = connectDatabase()
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `player` WHERE `TPFID` = %s"
            cursor.execute(sql, TPFID)
            result = cursor.fetchone()
        connection.commit()
    return bool(result['Whitelist'])

def inputNewPlayer(discordId, Steam64ID, whitelist):
    connection = connectDatabase()
    with connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `player` (`Steam64ID`, `DiscordID`, `Whitelist` ) VALUES (%s, %s, %s)"
            cursor.execute(sql, (int(Steam64ID),int(discordId),int(whitelist)))
        connection.commit()
    return