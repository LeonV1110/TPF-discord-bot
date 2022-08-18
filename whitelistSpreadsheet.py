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
