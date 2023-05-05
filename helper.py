from error import InvalidSteam64ID, InvalidDiscordID
import configparser

#Read in config file and set global variables
config = configparser.ConfigParser()
config.read('config.ini')
JUNIORADMINROLE = int(config['ADMINROLES']['JUNIOR'])
ADMINROLE = int(config['ADMINROLES']['ADMIN'])
SENIORADMINROLE = int(config['ADMINROLES']['SENIOR'])
DADMINROLE = int(config['ADMINROLES']['DADMIN'])
CAMROLE = int(config['ADMINROLES']['CAM'])
MVPROLE = int(config['WHITELISTROLES']['MVP'])
CREATORROLE = int(config['WHITELISTROLES']['CREATOR'])
WHITELISTROLE = int(config['WHITELISTROLES']['WHITELIST'])
FARMERROLE = int(config['WHITELISTROLES']['FARMER'])
COUNCILROLE = int(config['WHITELISTROLES']['COUNCIL'])
SHOWOFFROLE = int(config['WHITELISTROLES']['SHOWOFF'])

def convert_role_to_perm(roles):
    roles.reverse()
    for role in roles:
        if role.id == DADMINROLE: return 'dadmin'
        elif role.id == SENIORADMINROLE: return 'senior'
        elif role.id == ADMINROLE: return 'admin'
        elif role.id == JUNIORADMINROLE: return 'junior'
        elif role.id == CAMROLE: return 'cam'
        elif role.id == CREATORROLE: return 'creator'
        elif role.id == MVPROLE: return 'mvp'
    return None

def convert_role_to_tier(roles):
    roles.reverse()
    for role in roles:
        if role.id == SHOWOFFROLE: return 'show_off'
        elif role.id == COUNCILROLE: return 'council'
        elif role.id == FARMERROLE: return 'farmer'
        elif role.id == WHITELISTROLE: return 'whitelist'
    return None

def check_steam64ID(steam64ID: str):
    #check if int
    str(steam64ID)
    try:
        int(steam64ID)
    except:
        raise InvalidSteam64ID("A steam64ID contains just numbers.")
    #check if not default steam64ID
    if (steam64ID == str(76561197960287930)):
        raise InvalidSteam64ID("This is Gabe Newell's steam64ID, please make sure to enter the correct one.")
    #check if first numbers match
    if (not steam64ID[0:7] == "7656119"):
       raise InvalidSteam64ID("This is not a valid steam64ID.")
    #check the length
    if (len(steam64ID) < 17):
       raise InvalidSteam64ID("This is not a valid steam64ID, as it is shorter than 17 characters.")
    if (len(steam64ID) > 17):
        raise InvalidSteam64ID("This is not a valid steam64ID, as it is longer than 17 characters.")
    return 

def check_discordID(discordID: str):
    str(discordID)
    try:
        int(discordID)
    except:
        raise InvalidDiscordID('A discordID contains just numbers.')
    if len(discordID) < 17: 
        raise InvalidDiscordID("A discordID is 18 characters long, this one is too short.")
    elif len(discordID) > 18:
        raise InvalidDiscordID("A discordID is 18 characters long, this one is too long.")
    return

def get_max_whitelists(tier):
    tierDict = {'whitelist': 1, 'farmer': 2, 'council': 4, 'show_off': 10} #TODO update with acturate values
    return tierDict[tier]