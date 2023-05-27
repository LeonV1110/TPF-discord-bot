from database.database import excecute_query
from io import BytesIO

def getVIP():
    VIP_ls = process_whitelists()
    as_bytes = map(str.encode, VIP_ls)
    content = b"\n".join(as_bytes)
    return content

def get_whitelists():
    sql = "SELECT steam64ID, name FROM tpf_bot.player JOIN tpf_bot.whitelist ON tpf_bot.player.TPFID = tpf_bot.whitelist.TPFID;"
    vars = None
    res = excecute_query(sql, vars, 2)
    return res

def process_whitelists():
    ls = get_whitelists()
    res = adminBodge()
    for player in ls:
        steamid = player['steam64ID']
        name = player['name']
        res.append(f'{steamid} {name} 2223-05-13T19:34:32.270802')
    return res

def adminBodge():
    ls = [
    "76561197979668219 MoiDawg 2223-05-13T19:34:32.270802", 
    "76561198033230680 ST-HasBeen 2223-05-13T19:34:32.270802", 
    "76561198941431182 Xendu 2223-05-13T19:34:32.270802", 
    "76561198054860542 Raumdeuter 2223-05-13T19:34:32.270802", 
    "76561198292793058 Leon 2223-05-13T19:34:32.270802", 
    "76561198042411351 ImGrumpy 2223-05-13T19:34:32.270802", 
    "76561198055999243 cgee3 2223-05-13T19:34:32.270802", 
    "76561197960783537 shnu 2223-05-13T19:34:32.270802", 
    "76561198159748509 Matthijs 2223-05-13T19:34:32.270802", 
    "76561198080630985 SquidNinja 2223-05-13T19:34:32.270802", 
    "76561198381951164 Sullivan 2223-05-13T19:34:32.270802", 
    "76561198996775441 SoggyToast 2223-05-13T19:34:32.270802", 
    "76561198051753129 sheeps 2223-05-13T19:34:32.270802", 
    "76561198430173002 Babo 2223-05-13T19:34:32.270802", 
    "76561197961982019 Truckin 2223-05-13T19:34:32.270802", 
    "76561197973562026 CajunCO 2223-05-13T19:34:32.270802", 
    "76561198799199066 Treypool 2223-05-13T19:34:32.270802", 
    "76561198161952853 Shagira_Sidharta 2223-05-13T19:34:32.270802", 
    "76561198070760891 mikekerchooski 2223-05-13T19:34:32.270802", 
    "76561198141717776 valk 2223-05-13T19:34:32.270802", 
    "76561198225490248 tk_d1str1ct 2223-05-13T19:34:32.270802", 
    "76561198873443813 BLT 2223-05-13T19:34:32.270802", 
    "76561198353640082 Chewie 2223-05-13T19:34:32.270802", 
    "76561198817566265 TheHades 2223-05-13T19:34:32.270802", 
    "76561198022611097 Hawaiian 2223-05-13T19:34:32.270802", 
    "76561198307954786 EpiphanyStick 2223-05-13T19:34:32.270802", 
    "76561198020275971 krazy617 2223-05-13T19:34:32.270802", 
    "76561198991647035 DocROE 2223-05-13T19:34:32.270802", 
    "76561198240012158 Blair 2223-05-13T19:34:32.270802", 
    "76561198089381719 Deathknowz 2223-05-13T19:34:32.270802", 
    "76561198204121072 HaLone 2223-05-13T19:34:32.270802", 
    "76561198272190934 CBISH 2223-05-13T19:34:32.270802", 
    "76561198171365314 JakeMTN 2223-05-13T19:34:32.270802", 
    "76561198166563151 DeltaYork 2223-05-13T19:34:32.270802", 
    "76561198157726846 lateweevil 2223-05-13T19:34:32.270802", 
    "76561197970673331 fixie 2223-05-13T19:34:32.270802", 
    "76561198117718805 CommisarSpectre 2223-05-13T19:34:32.270802", 
    "76561199098817888 Jar18A4 2223-05-13T19:34:32.270802", 
    "76561198934246260 LoyalRevenge 2223-05-13T19:34:32.270802", 
    "76561198151895477 Stu 2223-05-13T19:34:32.270802", 
    "76561198134817587 probably_a_neko 2223-05-13T19:34:32.270802",  
    "76561197976184856 Owens 2223-05-13T19:34:32.270802", 
    "76561198289409271 Polarz 2223-05-13T19:34:32.270802", 
    "76561197961090585 SpacemanSpliff 2223-05-13T19:34:32.270802", 
    "76561198079323637 Shrek 2223-05-13T19:34:32.270802", 
    "76561197973222162 OldeBulldogge 2223-05-13T19:34:32.270802", 
    "76561198061533608 Greyhound 2223-05-13T19:34:32.270802", 
    "76561198866010765 HaftRat 2223-05-13T19:34:32.270802", 
    "76561198167734285 Akiyama 2223-05-13T19:34:32.270802", 
    "76561197961636884 zer0 2223-05-13T19:34:32.270802", 
    "76561198011574930 cjsjs 2223-05-13T19:34:32.270802", 
    "76561198074928236 PETE!!! 2223-05-13T19:34:32.270802", 
    "76561198091335408 Ender 2223-05-13T19:34:32.270802", 
    "76561198205216855 Snuffals 2223-05-13T19:34:32.270802", 
    "76561199011984242 TCOnline2 2223-05-13T19:34:32.270802", 
    "76561198162011414 DoeJoe 2223-05-13T19:34:32.270802", 
    "76561198045949633 reconjoe 2223-05-13T19:34:32.270802", 
    "76561198068902047 Peonanoob 2223-05-13T19:34:32.270802", 
    "76561198125837090 vortexman 2223-05-13T19:34:32.270802", 
    "76561198012851702 toasterKiller 2223-05-13T19:34:32.270802", 
    "76561198079579825 Lambda 2223-05-13T19:34:32.270802", 
    "76561198051436143 7777 2223-05-13T19:34:32.270802", 
    "76561198273467828 Bonsai 2223-05-13T19:34:32.270802", 
    "76561199089266567 EagleOne 2223-05-13T19:34:32.270802", 
    "76561198105794455 MadSquids 2223-05-13T19:34:32.270802", 
    "76561198073966891 MrIrrelevant 2223-05-13T19:34:32.270802", 
    "76561198997786416 N0ne 2223-05-13T19:34:32.270802", 
    "76561198267850988 OddChap_101 2223-05-13T19:34:32.270802", 
    "76561198156276927 Ronin_Man 2223-05-13T19:34:32.270802", 
    "76561198078555964 theUNSTABLE 2223-05-13T19:34:32.270802", 
    "76561198855309181 Baker 2223-05-13T19:34:32.270802", 
    "76561198008082182 nostaliga 2223-05-13T19:34:32.270802", 
    "76561198081313876 WX1K 2223-05-13T19:34:32.270802", 
    "76561198068406456 Wix 2223-05-13T19:34:32.270802", 
    "76561199160130821 SkyDawg 2223-05-13T19:34:32.270802", 
    "76561198964002257 HotelHandTowel 2223-05-13T19:34:32.270802", 
    "76561198049007431 Strieken 2223-05-13T19:34:32.270802", 
    "76561198383918715 Preslytax1600 2223-05-13T19:34:32.270802", 
    "76561198040162575 Oli 2223-05-13T19:34:32.270802", 
    "76561198443723014 Flour 2223-05-13T19:34:32.270802", 
    "76561198991959898 Classical 2223-05-13T19:34:32.270802", 
    "76561198125252597 AmericanSniper 2223-05-13T19:34:32.270802", 
    "76561198044259154 BigChungus 2223-05-13T19:34:32.270802", 
    "76561198048896027 gvstaylor1 2223-05-13T19:34:32.270802", 
    "76561199075743498 jagged 2223-05-13T19:34:32.270802", 
    "76561198320070061 mrpanda 2223-05-13T19:34:32.270802", 
    "76561198432940533 r2jcraniums 2223-05-13T19:34:32.270802", 
    "76561198115028854 radiantcanadian 2223-05-13T19:34:32.270802", 
    "76561198355350710 serv 2223-05-13T19:34:32.270802", 
    "76561198006188312 Vladdy 2223-05-13T19:34:32.270802", 
    "76561198121978404 ronin 2223-05-13T19:34:32.270802", 
    "76561199094812199 SwiggyRy 2223-05-13T19:34:32.270802", 
    "76561199012292564 Krystal 2223-05-13T19:34:32.270802", 
    "76561198264628239 EJ 2223-05-13T19:34:32.270802", 
    "76561199078885296 Chxos 2223-05-13T19:34:32.270802", 
    "76561198052379195 shadygoldfish 2223-05-13T19:34:32.270802", 
    "76561198898338941 EPOCCH 2223-05-13T19:34:32.270802", 
    "76561198449648040 KC7000 2223-05-13T19:34:32.270802", 
    "76561198012127027 Eofson 2223-05-13T19:34:32.270802", 
    "76561198328103024 Sureshot 2223-05-13T19:34:32.270802", 
    "76561198847125639 JK 2223-05-13T19:34:32.270802", 
    "76561198324144638 Tommykill 2223-05-13T19:34:32.270802", 
    "76561198024928805 Jamsheed 2223-05-13T19:34:32.270802", 
    "76561198896569403 Swaggyty 2223-05-13T19:34:32.270802"]
    return ls