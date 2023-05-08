from database.database import excecute_query

class Permission():
    TPFID: str
    permission: str

    def __eq__(self, __o: object) -> bool:
        return self.__dict__ == __o.__dict__
        
    def __init__(self, TPFID: str, permission: str):
        self.TPFID = TPFID
        self.permission = permission
        return

    def permission_to_DB(self):
        sql = "INSERT INTO `permission` (`TPFID`, `permission`) VALUES (%s, %s)"
        vars = (self.TPFID, self.permission)
        excecute_query(sql, vars)
        return

    def delete_permission(self):
        sql = "DELETE FROM `permission` WHERE `TPFID` = %s"
        vars = (self.TPFID)
        excecute_query(sql, vars)
        return

    def update_permission(self, permission: str):
        self.permission = permission
        sql = "UPDATE `permission` SET `permission` = %s WHERE `TPFID` = %s"
        vars = (permission, self.TPFID)
        excecute_query(sql, vars)
        return