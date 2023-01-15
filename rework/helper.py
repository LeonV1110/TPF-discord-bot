from error import InvalidSteam64ID

def convert_role_to_perm(roles):
    return #TODO

def convert_role_to_tier(roles):
    return #TODO

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