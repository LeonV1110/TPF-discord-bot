import database as db

def createWhitelistDoc():
    f = open("Whitelist doc\WhitelistDoc.txt", "w")
    f.write(createWhitelistString())
    f.close
    return

def createWhitelistString():
    whitelisters = db.getAllWhitelisters()
    result = ""
    for wl in whitelisters:
        result += createNewLine(wl["steam64ID"], wl["playerID"], wl["role"])
    return result

def createNewLine(steam64ID, TPFID, ROLE):
    line = "Admin=" + str(steam64ID) + ":" + str(ROLE) + " //" + str(TPFID) + " - added by TPFbot \n"
    return line