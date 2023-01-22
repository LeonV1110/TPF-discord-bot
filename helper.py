from error import InvalidSteam64ID, InvalidDiscordID
from dotenv import load_dotenv
import os


load_dotenv()

JUNIORADMINROLE = int(os.getenv('JUNIOR_ADMIN_ROLE'))
ADMINROLE = int(os.getenv('ADMIN_ROLE'))
SENIORADMINROLE = int(os.getenv('SENIOR_ADMIN_ROLE'))
DADMINROLE = int(os.getenv('DADMIN_ROLE'))
#CAMROLE = int(os.getenv('CAM_ROLE'))
#MVPROLE = int(os.getenv('MVP_ROLE'))
CREATORROLE = int(os.getenv('CREATOR_ROLE'))
WHITELISTROLE = int(os.getenv('WHITELIST_ROLE'))
FARMERROLE = int(os.getenv('FARMER_ROLE'))
COUNCILROLE = int(os.getenv('COUNCIL_ROLE'))
SHOWOFFROLE = int(os.getenv('SHOW_OFF_ROLE'))

def convert_role_to_perm(roles):
    roles.reverse()
    for role in roles:
        if role.id == DADMINROLE: return 'dadmin'
        elif role.id == SENIORADMINROLE: return 'senior'
        elif role.id == ADMINROLE: return 'admin'
        elif role.id == JUNIORADMINROLE: return 'junior'
        #elif role.id == CAMROLE: return 'cam'
        elif role.id == CREATORROLE: return 'creator'
        #elif role.id == MVPROLE: return 'MVP'
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
    if len(discordID) < 18: 
        raise InvalidDiscordID("A discordID is 18 characters long, this one is too short.")
    elif len(discordID) > 18:
        raise InvalidDiscordID("A discordID is 18 characters long, this one is too long.")
    return

def get_max_whitelists(tier):
    tierDict = {'whitelist': 1, 'farmer': 1, 'council': 1, 'show_off': 1} #TODO update with acturate values
    return tierDict[tier]