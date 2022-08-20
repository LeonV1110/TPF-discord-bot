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
        result += createNewLine(wl["Steam64ID"], wl["Name"])
    return result

def createNewLine(steam64ID, name):
    line = "Admin=" + str(steam64ID) + ":whitelist //" + name + " - added by TPFbot \n"
    return line