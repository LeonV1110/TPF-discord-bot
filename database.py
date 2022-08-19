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

def getWhitelistStatus(connection, discordId, TPFID):
    with connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `player` WHERE `TPFID` = %s"
            cursor.execute(sql, TPFID)
            result = cursor.fetchone()
        connection.commit()
    return bool(result['Whitelist'])

def inputNewPlayer(connection):
    with connection:
        with connection.cursor() as cursor:
            sql = "INSERT INTO `player` (`TPFID`, `Steam64ID`, `DiscordID`, `Whitelist` ) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (int(3),int(3),int(3),int(0)))
        connection.commit()
    return

connection= connectDatabase()
print(connection.open)
#inputNewPlayer(connection)
print(getWhitelistStatus(connection, 1,3))
