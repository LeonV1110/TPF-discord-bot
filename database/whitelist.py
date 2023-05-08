from database.database import excecute_query

class Whitelist():
    TPFID: str
    orderID: str

    def __eq__(self, __o: object) -> bool:
        return self.__dict__ == __o.__dict__
    
    def __init__(self, TPFID: str, orderID: str):
        self.TPFID = TPFID
        self.orderID = orderID
        return

    def whitelist_to_DB(self):
        sql = "INSERT INTO `whitelist` (`TPFID`, `orderID`) VALUES (%s, %s)"
        vars = (self.TPFID, self.orderID)
        excecute_query(sql, vars)
        return

    def delete_whitelist(self):
        sql = "DELETE FROM `whitelist` WHERE `TPFID` = %s"
        vars = (self.TPFID)
        excecute_query(sql, vars)
        return

    def update_whitelist(self, orderID: str):
        self.orderID = orderID
        sql = "UPDATE `whitelist` SET `orderID` = %s WHERE `TPFID` = %s"
        vars = (orderID, self.TPFID)
        excecute_query(sql, vars)
        return