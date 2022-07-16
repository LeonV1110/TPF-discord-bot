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
    checkMemberWhitelist("JSquad81#9733")
    return

def checkMemberWhitelist(discordName):
    whitelisters = df.loc[df['group'] == 'whitelist']
    user = whitelisters.loc[whitelisters['discord username'] == discordName ]
    if (str(user.steamid) != ""):
        return True
    return False