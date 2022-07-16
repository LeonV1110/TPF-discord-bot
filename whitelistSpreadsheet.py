import pygsheets
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLEBOT = os.getenv("GOOGLE_BOT_FILE")

gc = pygsheets.authorize(service_account_file=GOOGLEBOT)
sheet = gc.open('testnaam')
wks = sheet[0]
df = wks.get_as_df()


def test():
    print(df.columns)
    print(checkMemberWhitelist("Jyoshikai#6778"))
    return

def checkMemberWhitelist(discordName):
    whitelisters = df.loc[df['group'] == 'whitelist']
    user = whitelisters.loc[whitelisters['discord username'] == discordName ]
    
    if (user.empty):
        return False
    elif not (user.steamid.empty):
        return True
    return False
