from dotenv import load_dotenv
import os
import pymysql
import errors as err
import whitelistDoc as wd

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
    return

def setupPlayerTable():
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = """CREATE TABLE `tpf_new`.`player` (
                    `playerID` INT NOT NULL AUTO_INCREMENT,
                    `name` VARCHAR(45) NOT NULL,
                    `steam64ID` BIGINT NOT NULL,
                    `discordID` BIGINT NOT NULL,
                    `role` VARCHAR(20) NULL,
                    `patreonID` VARCHAR(45) NULL,
                    PRIMARY KEY (`playerID`));"""
            cursor.execute(sql)
        connection.commit()
    return

#############################
######### getters ###########
#############################

#Gets the player by either discordID, steam64ID or playerID, with the discordID taking priority.
#raises PlayerNotFound exception
def getPlayer(discordID = None, steam64ID = None, playerID = None):
    if discordID != None:
        return getPlayerByDiscordID(discordID)
    elif steam64ID != None:
        return getPlayerBySteam64ID(steam64ID)
    elif playerID != None:
        return getPlayerByPlayerID(playerID)
    raise err.PlayerNotFound(message = "No ID provided")

def getPlayerByDiscordID(discordID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `player` WHERE `discordID` = %s "
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
            sql = "SELECT * FROM `player` WHERE `steam64ID` = %s "
            cursor.execute(sql, steam64ID)
            result = cursor.fetchone()
        connection.commit()
    if bool(result):
        return result
    else:
        raise err.PlayerNotFound(message = "There is no player with this steam64ID")

def getPlayerByPlayerID(playerID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `player` WHERE `playerID` = %s "
            cursor.execute(sql, playerID)
            result = cursor.fetchone()
        connection.commit()
    if bool(result):
        return result
    else:
        raise err.PlayerNotFound("There is no player with this playerID")

#returns a dictionary containing all the rows where the player has whitelist
#TODO deal with roles above whitelist
def getAllWhitelisters():
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `player` WHERE `role` = \"whitelist\""
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
            sql = "SELECT * FROM `player` WHERE `steam64ID` = %s"
            cursor.execute(sql, steam64ID)
        connection.commit()
        result = cursor.fetchone()
    return bool(result)

def checkDiscordIDPressence(discordID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `player` WHERE `discordID` = %s"
            cursor.execute(sql, discordID)
        connection.commit()
        result = cursor.fetchone()
    return bool(result)

#############################
######### inputs ############
#############################

#inputs a new player into the database
#returns the generated playerID
def inputNewPlayer(discordID, steam64ID, role, name):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `player` (`steam64ID`, `discordID`, `role`, `name`) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (steam64ID, discordID, role, name))
        with connection.cursor() as cursor:
            sql = "SELECT `playerID` FROM `player` WHERE `discordID` = %s"
            cursor.execute(sql, discordID)
            result = cursor.fetchone()
        connection.commit()
    wd.createWhitelistDoc()
    return result['playerID']

##############################
######### updates ############
##############################

def updateRole(role, discordID):
    updateRoleNoDoc(role, discordID)
    wd.createWhitelistDoc()
    return

def updateRoleNoDoc(role, discordID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "UPDATE `player` SET `role` = %s WHERE `discordID` = %s"
            cursor.execute(sql, (role, discordID))
        connection.commit()
    return
##############################
######### deleters ###########
##############################

def deletePlayer(discordID = None, steam64ID = None, playerID = None):
    if discordID != None:
        return deletePlayerByDiscordID(discordID)
    elif steam64ID != None:
        return deletePlayerBySteam64ID(steam64ID)
    elif playerID != None:
        return deleteplayerByPlayerID(playerID)
    raise err.PlayerNotFound(message = "Make sure to pass at least one ID")

def deletePlayerByDiscordID(discordID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "DELETE FROM `player` WHERE `discordID` = %s"
            cursor.execute(sql, discordID)
        connection.commit()

def deletePlayerBySteam64ID(steam64ID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "DELETE FROM `player` WHERE `steam64ID` = %s"
            cursor.execute(sql, steam64ID)
        connection.commit()

def deleteplayerByPlayerID(playerID):
    with connectDatabase() as connection:
        with connection.cursor() as cursor:
            sql = "DELETE FROM `player` WHERE `playerID` = %s"
            cursor.execute(sql, playerID)
        connection.commit()