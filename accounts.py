from account import Account
import services
import sqlite3

class Accounts:

    def __init__(self, where: str, order_by: str):
        self._where = where
        self._order_by = order_by
        self._select_account = None

        data = Data()

        self._accounts = list()
        for record in data.query(self._where, self._order_by):
            self._accounts.append(Account(record))

    def get_account_at(self, i: int) -> Account:
        self._select_account = self._accounts[i]
        return self._accounts[i]
    
    def get_selected_account(self):
        return self._select_account

    def get_accounts(self) -> list:
        return self._accounts



        
    ###############################################
    ## GET_ACCOUNT_LIST
    ## Return tuple of string months (Januaury,....)
    ################################################
    # def get_account_list() -> tuple:
    #     return tuple(data.query_distinct_account_name())


class Data:

    def query(self, where: str, order_by: str) -> tuple:
        if where == None:
            where = ""
        else:
            where = f"WHERE {where}"
        if order_by == None:
            order_by = "ORDER BY name"
        else:
            order_by = f"ORDER BY {order_by}"

        conn = sqlite3.connect(services.get_db_file())
        sql_cursor = conn.cursor()
        sql_cursor.execute(f"""
            select * from account {where} {order_by}
        """,
        {})
        
        records = sql_cursor.fetchall()
        conn.close()   
        
        return tuple(records)             