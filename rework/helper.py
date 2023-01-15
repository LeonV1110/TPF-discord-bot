from error import InvalidSteam64ID
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
    try:
        int(steam64ID)
    except:
        raise InvalidSteam64ID("A steam64ID contains just numbers.")
    #check if not default steam64ID
    if (steam64ID == str(76561197960287930)):
        raise InvalidSteam64ID("This is Gabe Newell's steam64ID, please make sure to enter yours.")
    #check if first numbers match
    if (not steam64ID[0:7] == "7656119"):
       raise InvalidSteam64ID("This is not a valid steam64ID.")
    #check the length
    if (len(str(steam64ID)) < 17):
       raise InvalidSteam64ID("This is not a valid steam64ID, as it is shorter than 17 characters.")
    if (len(str(steam64ID)) > 17):
        raise InvalidSteam64ID("This is not a valid steam64ID, as it is longer than 17 characters.")
    return 