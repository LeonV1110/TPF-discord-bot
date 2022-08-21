import pygsheets
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLEBOT = os.getenv("GOOGLE_BOT_FILE")


def opensheet():
    gc = pygsheets.authorize(service_account_file=GOOGLEBOT)
    sheet = gc.open('Players')
    wks = sheet[0]
    df = wks.get_as_df()
    return df

def test():
    df = opensheet()
    print(df.columns)
    print(checkMemberWhitelist("Jyoshikai#6778"))
    return

def checkListWhitelist(toCheck):
    df = opensheet()
    hasWhitelist = []
    for name in toCheck:
        if (checkMemberWhitelist(name, df)):
            hasWhitelist.append(name)

    return hasWhitelist
        
def checkMemberWhitelist(discordName, df):
    
    whitelisters = df.loc[df['group'] == 'whitelist']
    user = whitelisters.loc[whitelisters['discord username'] == discordName ]
    
    if (user.empty):
        return False
    elif not (user.steamid.empty):
        return True
    return False

def openWks():
    gc = pygsheets.authorize(service_account_file=GOOGLEBOT)
    sheet = gc.open('Players')
    wks = sheet[0]
    return wks

def updateDiscordID(wks, discordName, discordID):
    
    cell = wks.find(discordName, cols= (6,6) )
    if (not cell): return #check if the user is in the database
    
    row = cell[0].row
    addr = "k" + str(row)
    print(addr)
    wks.update_value(addr, str(discordID))
    return


def getUsernameSteamIDDisID():
    df = opensheet()
    users = df[['discord username', 'steamid', 'DiscordID']]
    return users

def countWhitelist():
    df = opensheet()
    whitelisters = df.loc[df['group'] == 'whitelist']
    return len(whitelisters)

def getAllWhitelist():
    df = opensheet()
    whitelisters = df.loc[df['group'] == 'whitelist']
    return whitelisters
