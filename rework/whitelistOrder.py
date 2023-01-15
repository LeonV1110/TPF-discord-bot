import random

from database import excecute_query
from whitelist import Whitelist


class WhitelistOrder():
    TPFID: str
    orderID: str
    tier: str #TODO, maybe make into a tierclass instead of a String
    whitelists: list[Whitelist]

    def __init__(self, TPFID: str, orderID: str, tier: str, whitelists: list[Whitelist] = []):
        self.TPFID = TPFID
        self.orderID = orderID
        self.tier = tier
        self.whitelists = whitelists
        return

    def order_to_DB(self):
        sql = "INSERT INTO `whitelist_order` (`orderID`, `TPFID`, `tier`) VALUES (%s, %s, %s)"
        vars = (self.orderID, self.TPFID, self.tier)
        excecute_query(sql, vars)

        owner_whitelist = Whitelist(self.TPFID, self.orderID)
        owner_whitelist.whitelist_to_DB()
        return

    def delete_order(self): # should also delete any whitelist orders
        for whitelist in self.whitelists:
            whitelist.delete_whitelist()
        
        sql = "DELETE FROM `whitelist_order` WHERE `orderID` = %s"
        vars = (self.orderID)
        excecute_query(sql, vars)
        return

    def update_order_tier(self, tier: str = None):
        sql = "UPDATE `whitelist_order` SET `tier`= %s WHERE `TPFID` = %s"
        vars = (tier, self.TPFID)
        excecute_query(sql, vars)
        return

    def add_whitelist(self, TPFID: str):
        whitelist = Whitelist(TPFID, self.orderID)
        whitelist.whitelist_to_DB()
        return

class NewWhitelistOrder(WhitelistOrder):
    def __init__(self, TPFID: str,tier: str):
        orderID = NewWhitelistOrder.__generate_orderID()
        super().__init__(TPFID, orderID, tier, [])
        return
    
    @staticmethod
    def __generate_orderID()-> str:
        orderID: int = 1
        while orderID == 1 or NewWhitelistOrder.__check_orderID_pressence(orderID):
            orderID = random.randint(1111111111111111, 9999999999999999) #16 long ID
        return str(orderID)
    
    @staticmethod
    def __check_orderID_pressence(orderID)-> bool:
        sql = "SELECT * FROM `whitelist_order` WHERE `orderID` = %s"
        vars = (orderID)
        res = excecute_query(sql, vars, 1)
        return bool(res)

class DatabaseWhitelistOrder(WhitelistOrder):
    def __init__(self, TPFID: str):
        sql = "SELECT * FROM `whitelist_order` WHERE `TPFID` = %s"
        vars = (TPFID)
        order_list = excecute_query(sql, vars, 1)
        orderID = order_list['orderID']
        tier = order_list['tier']
        whitelists = DatabaseWhitelistOrder.get_all_whitelists(orderID)
        super().__init__(TPFID, orderID, tier, whitelists)

    @staticmethod
    def get_all_whitelists(orderID) -> list[Whitelist]:
        sql = "select * from `whitelist` where `orderID` = %s"
        vars = (orderID)
        res = excecute_query(sql, vars, format= 2)
        wl_list = []
        for wl_dict in res:
            whitelist = Whitelist(wl_dict['TPFID'], wl_dict['orderID'])
            wl_list.append(whitelist)
        return whitelist