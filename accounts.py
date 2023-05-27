from account import Account
import services
import sqlite3

class Accounts:
          
    def get_all_accounts(self) -> list:
        
        data = Data()

        accounts = list()
        print()
        for record in data.query_all_accounts():
            accounts.append(Account(record))

        return accounts



        
    ###############################################
    ## GET_ACCOUNT_LIST
    ## Return tuple of string months (Januaury,....)
    ################################################
    # def get_account_list() -> tuple:
    #     return tuple(data.query_distinct_account_name())


class Data:

    def query_all_accounts(self) -> tuple:
        conn = sqlite3.connect(services.get_db_file())
        sql_cursor = conn.cursor()
        sql_cursor.execute("""
            select * from account order by name
        """,
        {})
        
        records = sql_cursor.fetchall()
        conn.close()   
        
        return tuple(records)             