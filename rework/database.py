from dotenv import load_dotenv
import os
import pymysql

load_dotenv()
DATABASEUSER = os.getenv('DATABASE_USERNAME')
DATABASEPSW = os.getenv('DATABASE_PASSWORD')
DATABASEHOST = os.getenv('DATABASE_HOST')
DATABASENAME = os.getenv('DATABASE_NAME')


def connect_database() -> pymysql.connections.Connection:
    connection = pymysql.connect(host=DATABASEHOST, user = DATABASEUSER, password= DATABASEPSW, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, database=DATABASENAME)
    return connection

def excecute_query(sql: str, vars: tuple = None, format: int = 3):
    with connect_database() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, vars)
            if format == 1: result = cursor.fetchone()
            elif format == 2: result = cursor.fetchall()
        connection.commit()
    if format == 3: return
    elif bool(result):
        return result
    else: return #TODO, figure out what to do when the database return nothing

def setup_database():
    setup_player_table()
    setup_order_table()
    setup_whitelist_table()
    setup_permission_table()
    return

def setup_player_table():
    sql = """CREATE TABLE `player` (
        `TPFID` varchar(15) NOT NULL,
        `steam64ID` varchar(17) NOT NULL,
        `discordID` varchar(18) NOT NULL,
        `name` varchar(45) NOT NULL,
        `patreonID` varchar(45) DEFAULT NULL COMMENT 'Currently not used',
        PRIMARY KEY (`TPFID`))"""
    excecute_query(sql)

def setup_order_table():
    sql = """CREATE TABLE `whitelist_order` (
        `orderID` varchar(16) NOT NULL,
        `TPFID` varchar(15) NOT NULL,
        `tier` varchar(45) NOT NULL,
        PRIMARY KEY (`OrderID`))"""
    excecute_query(sql)

def setup_whitelist_table():
    sql = """CREATE TABLE `whitelist` (
        `orderID` varchar(16) NOT NULL,
        `TPFID` varchar(15) NOT NULL,
        PRIMARY KEY (`OrderID`, `TPFID`))"""
    excecute_query(sql)

def setup_permission_table():
    sql = """CREATE TABLE `permission` (
        `TPFID` varchar(15) NOT NULL,
        `permission` varchar(45) NOT NULL,
        PRIMARY KEY (`TPFID`))"""
    excecute_query(sql)

