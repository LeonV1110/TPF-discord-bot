def checkSteam64ID(steamID):
    #check if int
    try:
        int(steamID)
    except:
        return "A steam64ID contains just numbers."
    #check if not default steam64ID
    if (steamID == 76561197960287930):
        return "This is Gabe Newell's steam64ID, please make sure to enter yours."
    stringID = str(steamID)
    #check if first numbers match
    if (not stringID[0:7] == "7656119"):
        return "This is not a valid steam64ID."

    return "suc6"