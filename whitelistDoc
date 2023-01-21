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
    else: return

def create_doc():
    f = open("Whitelist doc\WhitelistDoc.txt", "w")
    
    whitelist_lines = get_whitelist_lines()
    permission_lines = get_permission_lines()
    lines = permission_lines + whitelist_lines

    for line in lines:
        f.write(line)
    f.close
    return

def create_new_line(steam64ID, TPFID, role):
    line = "Admin=" + str(steam64ID) + ":" + str(role) + " //" + str(TPFID) + " - added by TPFbot \n"
    return line

def get_whitelist_lines():
    sql = "select player.steam64ID, player.TPFID from `player` join `whitelist` on player.TPFID= whitelist.TPFID"
    whitelists = excecute_query(sql, None, 2)
    lines = []
    for whitelist in whitelists:
        line = create_new_line(whitelist['steam64ID'], whitelist['TPFID'], 'whitelist')
        lines.append(line)
    return lines

def get_permission_lines():
    sql = "select player.steam64ID, player.TPFID, permission.permission from `player` join `permission` on player.TPFID= permission.TPFID;"
    permissions = excecute_query(sql, None, 2)
    lines = []
    for perm in permissions:
        line = create_new_line(perm['steam64ID'], perm['TPFID'], perm['permission'])
        lines.append(line)
    return lines

create_doc()