import pygsheets
import pandas as pd
import disnake
from player import NewPlayer
import helper as hlp
from error import MyException, PlayerNotFound
import configparser

#Read in config file and set global variables
config = configparser.ConfigParser()
config.read('config.ini')
GOOGLEBOT = config['GOOGLE']['GOOGLEBOT']
GUILD = config['DISCORD']['GUILD']

def get_sheet() -> pd.DataFrame:
    gc = pygsheets.authorize(service_account_file=GOOGLEBOT)
    sheet = gc.open('Players')
    wks = sheet[0]
    df = wks.get_as_df()
    return df

def import_spreadsheet(bot):
    df = get_sheet()

    length = len(df)
    nameSeries = df['discord username'].squeeze()
    steam64IDSeries = df['steamid'].squeeze()
    discordIDSeries = df['DiscordID'].squeeze()
    groupSeries = df['group']

    AllowedGroups = ['whitelist', 'mvp', 'creator', 'caster' ]
    count = 0

    guild = disnake.utils.get(bot.guilds, name = GUILD)
    members = [member for member in guild.members]

    for i in range(length):
        group = groupSeries.at[i]
        if group in AllowedGroups:
            name = nameSeries.at[i]
            discordID = discordIDSeries.at[i]
            steam64ID = steam64IDSeries.at[i]
            permission = None #TODO give permission role in discord if on spreadsheet.
            if group == 'mvp':
                permission = 'MVP' 
            elif group == 'creator' or group == 'caster':
                permission =  'creator'

            try:
                member = get__member(bot, discordID)

                tier = hlp.convert_role_to_tier(member.roles)
                name = member.name + "#" + member.discriminator
                if permission is None:
                    permission = hlp.convert_role_to_perm(member.roles)
                player = NewPlayer(steam64ID, discordID, name, permission, tier)
                player.player_to_DB()
            except PlayerNotFound as error:
                print(error.message + name)
            except MyException as error:
                print(error.message)
            except:
                pass #TODO more error handling

def get__member(bot, discordID):
    guild = disnake.utils.get(bot.guilds, name = GUILD)
    members = [member for member in guild.members]
    for member in members:
        if member.id == discordID:
            return member
    raise PlayerNotFound

    