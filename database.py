import re
from dotenv import load_dotenv
import os
import pymysql as mySQL
import errors as err

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
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `player` WHERE `TPFID` = %s"
            cursor.execute(sql, TPFID)
            result = cursor.fetchone()
        connection.commit()
    return bool(result['Whitelist'])

def inputNewPlayer(discordID, steam64ID, whitelist):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `player` (`Steam64ID`, `DiscordID`, `Whitelist` ) VALUES (%s, %s, %s)"
            cursor.execute(sql, (int(steam64ID),int(discordID),int(whitelist)))
        with connection.cursor() as cursor:
            sql = "SELECT `TPFID` FROM `player` WHERE `Steam64ID` = %s"
            cursor.execute(sql, int(steam64ID))
            result = cursor.fetchone()
            
        connection.commit()
    return result['TPFID']

def checkSteamIDPressence(steam64ID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `player` WHERE `Steam64ID` = %s"
            cursor.execute(sql, steam64ID)
        connection.commit()
        result = cursor.fetchone()
    return bool(result)

def checkDiscordIDPressence(discordID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `player` WHERE `DiscordID` = %s"
            cursor.execute(sql, discordID)
        connection.commit()
        result = cursor.fetchone()
    return bool(result)

def getPlayerByTPFID(TPFID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `player` WHERE `TPFID` = %s"
            cursor.execute(sql, TPFID)
            result = cursor.fetchone()
        connection.commit()
    return result

def getPlayerByDiscordID(discordID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `player` WHERE `DiscordID` = %s"
            cursor.execute(sql, discordID)
            result = cursor.fetchone()
        connection.commit()
    return result
