from dotenv import load_dotenv
import os
import pymysql
import errors_new as err

load_dotenv()
DATABASEUSER = os.getenv('DATABASE_USERNAME')
DATABASEPSW = os.getenv('DATABASE_PASSWORD')
DATABASEHOST = os.getenv('DATABASE_HOST')
DATABASENAME = os.getenv('DATABASE_NAME')

#############################
######### setup #############
#############################

def connectDatabase():
    connection = pymysql.connect(host=DATABASEHOST, user = DATABASEUSER, password= DATABASEPSW, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, database=DATABASENAME)
    return connection

def setupDatabase():
    setupPlayerTable()
    setupOrderTable()
    return

def setupPlayerTable():
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = """CREATE TABLE `player` (
                `TPFID` bigint NOT NULL,
                `Steam64ID` bigint NOT NULL,
                `DiscordID` bigint NOT NULL,
                `Name` varchar(45) NOT NULL,
                `PatreonID` bigint DEFAULT NULL COMMENT 'Currently not used',
                `Permission` varchar(45) NOT NULL,
                `Whitelist` bigint DEFAULT NULL,
                PRIMARY KEY (`TPFID`))"""
            cursor.execute(sql)
        connection.commit()
    return

def setupOrderTable():
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = """CREATE TABLE `whitelistorder` (
                `OrderID` bigint NOT NULL,
                `TPFID` bigint NOT NULL,
                `Tier` varchar(45) NOT NULL DEFAULT 'Solo',
                `Active` TINYINT NOT NULL,
                `Whitelistees` INT NOT NULL DEFAULT 1,
                PRIMARY KEY (`OrderID`))"""
            cursor.execute(sql)
        connection.commit()  

#############################
######### getters ###########
#############################

#Gets the player by either discordID, steam64ID or playerID, with the discordID taking priority.
#raises PlayerNotFound exception
def getPlayer(discordID = None, steam64ID = None, TPFID = None):
    if discordID != None:
        return getPlayerByDiscordID(discordID)
    elif steam64ID != None:
        return getPlayerBySteam64ID(steam64ID)
    elif TPFID != None:
        return getPlayerByTPFID(TPFID)
    raise err.PlayerNotFound(message = "No ID provided")

def getPlayerByDiscordID(discordID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `player` WHERE `DiscordID` = %s "
            cursor.execute(sql, discordID)
            result = cursor.fetchone()
        connection.commit()
    if bool(result):
        return result
    else:
        raise err.PlayerNotFound(message = "There is no player with this discordID")

def getPlayerBySteam64ID(steam64ID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `player` WHERE `Steam64ID` = %s "
            cursor.execute(sql, steam64ID)
            result = cursor.fetchone()
        connection.commit()
    if bool(result):
        return result
    else:
        raise err.PlayerNotFound(message = "There is no player with this steam64ID")

def getPlayerByTPFID(TPFID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `player` WHERE `TPFID` = %s "
            cursor.execute(sql, TPFID)
            result = cursor.fetchone()
        connection.commit()
    if bool(result):
        return result
    else:
        raise err.PlayerNotFound("There is no player with this TPF-ID")  

#returns a dictionary containing all the rows where the player has whitelist
def getAllWhitelisters():
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `player` WHERE `Whitelist` IS NOT NULL"
            cursor.execute(sql)
            result = cursor.fetchall()
        connection.commit()
    return result

def getWhitelistOrder(TPFID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `whitelistorder` WHERE `TPFID` = %s"
            cursor.execute(sql, TPFID)
            result = cursor.fetchall()
        connection.commit()
    return result

def getAllPlayersOnOrder(OrderID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `whitelistorder` WHERE `Whitelistees` = %s"
            cursor.execute(sql, OrderID)
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

def checkTPFIDPressence(TPFID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `player` WHERE `TPFID` = %s"
            cursor.execute(sql, TPFID)
        connection.commit()
        result = cursor.fetchone()
    return bool(result)

def checkOrderIDPressence(orderID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `whitelistorder` WHERE `OrderID` = %s"
            cursor.execute(sql, orderID)
        connection.commit()
        result = cursor.fetchone()
    return bool(result)

def checkTPFIDPressenceInOrder(TPFID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `whitelistorder` WHERE `TPFID` = %s"
            cursor.execute(sql, TPFID)
        connection.commit()
        result = cursor.fetchone()
    return bool(result)

#############################
######### inputs ############
#############################

#inputs a new player into the database
def inputNewPlayer(TPFID, discordID, steam64ID, permission, name, patreonID = None): #patreonID is not currently used
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `player` (`TPFID`, `Steam64ID`, `DiscordID`, `Name`, `Permission`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (TPFID, steam64ID, discordID, name, permission))
        connection.commit()
    return

#inputs a new whitelist order to the database
def inputWhiteListOrder(orderID, TPFID, tier, active, whitelistees):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `whitelistorder` (`OrderID`, `TPFID`, `Tier`, `Active`, `Whitelistees`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (str(orderID), str(TPFID), str(tier), int(active), str(whitelistees)))
        connection.commit()
    return

##############################
######### updates ############
##############################

#adds the whitelist to the user
def updateWhiteList(TPFID, orderID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "UPDATE `player` SET `Whitelist` = %s WHERE `TPFID` = %s"
            cursor.execute(sql, (orderID, TPFID))
        connection.commit()
    return

#updates the perssion of the user
def updatePermission(TPFID, permission):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "UPDATE `player` SET `Permission` = %s WHERE `TPFID` = %s"
            cursor.execute(sql, (permission, TPFID))
        connection.commit()
    return

def updateTier(orderID, tier):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "UPDATE `whitelistorder` SET `Tier` = %s WHERE `OrderID` = %s"
            cursor.execute(sql, (tier, orderID))
        connection.commit()
    return

def updateWhitelistees(orderID, whitelistees):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "UPDATE `whitelistorder` SET `Whitelistees` = %s WHERE `OrderID` = %s"
            cursor.execute(sql, (whitelistees, orderID))
        connection.commit()
    return

def updateActivity(orderID, activity):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "UPDATE `whitelistorder` SET `Activity` = %s WHERE `OrderID` = %s"
            cursor.execute(sql, (activity, orderID))
        connection.commit()
    return

##############################
######### deleters ###########
##############################

def deletePlayer(discordID = None, steam64ID = None, TPFID = None):
    if discordID != None:
        return deletePlayerByDiscordID(discordID)
    elif steam64ID != None:
        return deletePlayerBySteam64ID(steam64ID)
    elif TPFID != None:
        return deleteplayerByTPFID(TPFID)
    raise err.PlayerNotFound(message = "Make sure to pass at least one ID")

def deletePlayerByDiscordID(discordID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "DELETE FROM `player` WHERE `DiscordID` = %s"
            cursor.execute(sql, discordID)
        connection.commit()
    return

def deletePlayerBySteam64ID(steam64ID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "DELETE FROM `player` WHERE `Steam64ID` = %s"
            cursor.execute(sql, steam64ID)
        connection.commit()
    return

def deleteplayerByTPFID(TPFID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "DELETE FROM `player` WHERE `TPFID` = %s"
            cursor.execute(sql, TPFID)
        connection.commit()
    return

def deleteWhitelistOrder(orderID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "DELETE FROM `whitelistorder` WHERE `OrderID` = %s"
            cursor.execute(sql, orderID)
        connection.commit()
    return