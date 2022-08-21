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
    
#############################
######### getters ###########
#############################

def getPlayerByTPFID(TPFID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `player` WHERE `TPFID` = %s"
            cursor.execute(sql, TPFID)
            result = cursor.fetchone()
        connection.commit()
    if bool(result):
        return result
    else:
        raise err.PlayerNotFound()

def getPlayerByDiscordID(discordID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `player` WHERE `DiscordID` = %s"
            cursor.execute(sql, discordID)
            result = cursor.fetchone()
        connection.commit()
    if bool(result):
        return result
    else:
        raise err.PlayerNotFound()

def getWhitelistStatus(discordId):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `player` WHERE `DiscordID` = %s"
            cursor.execute(sql, discordId)
            result = cursor.fetchone()
        connection.commit()
    return bool(result['Whitelist'])

def getAllWhitelisters():
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `player` WHERE `Whitelist` = True"
            cursor.execute(sql)
            result = cursor.fetchall()
        connection.commit()
    return result
    
#############################
######### checkers ##########
#############################

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

##############################
######### setters ############
##############################

def updateWhitelist(whitelist, steam64ID, discordID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "UPDATE `player` SET `Whitelist` = %s WHERE `Steam64ID` = %s AND `DiscordID` = %s"
            cursor.execute(sql, (whitelist, steam64ID, discordID))
        connection.commit()
    return

def inputNewPlayer(discordID, steam64ID, whitelist, name):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `player` (`Steam64ID`, `DiscordID`, `Whitelist`, `Name`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (steam64ID,discordID,whitelist, name))
        with connection.cursor() as cursor:
            sql = "SELECT `TPFID` FROM `player` WHERE `Steam64ID` = %s"
            cursor.execute(sql, int(steam64ID))
            result = cursor.fetchone()
            
        connection.commit()
    return result['TPFID']

def updateDiscordID(discordID, TPFID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "UPDATE `player` SET `DiscordID` = %s WHERE `TPFID` = %s"
            cursor.execute(sql, (discordID, TPFID))
        connection.commit()
    return

##############################
######### deleters ###########
##############################

def deletePlayer(discordID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "DELETE FROM `player` WHERE `DiscordID` = %s"
            cursor.execute(sql, discordID)
        connection.commit()
    return 