import os
import sqlite3

#####################################################
#####################################################    
def get_db_file():
    return os.path.join(os.getcwd(), "bills.db")

#####################################################
#####################################################    
def initilize_month_sql(year, month):
    conn = sqlite3.connect(get_db_file())
    sql_cursor = conn.cursor()
    sql_cursor.execute("""
        insert into bill (amount, account_id,year,month,payment_confirmed)
        select def_amt, id,:year,:month, 0
        from account
        where (ifnull(month,'') = '' or  month = :month)
        and ifnull(active,0) = 1
        and id not in (select account_id from  bill where month = :month and year = :year);
    """,
    {
        'year':year,
        'month':month
    })

    conn.commit()
    conn.close() 

def get_bill_list(year, month):
    # due_date2, account_id, note are hidden in treeview 
    # due_date2 is only used for order, Be sure to leave it at the end of sql
    # strftime('%m/%d/%Y',bill.dt_paid)
    conn = sqlite3.connect(get_db_file())
    sql_cursor = conn.cursor()
    sql_cursor.execute("""
        select account.id, account.name, bill.amount, strftime('%Y-%m-%d',bill.dt_paid) dt_paid,  
        bill.payment_confirmed,
        :month || '/' || account.due_dom || '/' || :year due_dom1, 0 ytd, 0 last_bill, 
        0 last_year, account.due_dom due_dom2, bill.note
        from bill
        inner join account on account.id = bill.account_id
        where bill.year = :year
            and bill.month = :month
        order by account.due_dom
    """,
    {
        'year':year,
        'month':month
    })
    
    records = sql_cursor.fetchall()
    conn.close()   
    
    return records  

def query_distinct_account_name():
    conn = sqlite3.connect(get_db_file())
    sql_cursor = conn.cursor()
    sql_cursor.execute("""
        select account.name from account order by name
    """,
    {})
    
    records = sql_cursor.fetchall()
    conn.close()   

    print(records)
    
    return records  

#####################################################
#####################################################    
def save_bill(year, month, account_id, amount, note, dt_paid, payment_confirmed):
    # print(f"dt_paid:{dt_paid}")
    conn = sqlite3.connect(get_db_file())
    sql_cursor = conn.cursor()
    sql_cursor.execute("""
        update bill
            set amount =  :amount,
                note = :note,
                dt_paid = date(:dt_paid),
                payment_confirmed = :payment_confirmed
        where month = :month
        and year = :year
        and account_id= :account_id;
    """,
    {
        'year':year,
        'month':month,
        'account_id':account_id,
        'amount':amount,
        'note':note,
        'dt_paid':dt_paid,
        'payment_confirmed':payment_confirmed
    })

    conn.commit()
    conn.close() 

def create_db():
    conn = sqlite3.connect(get_db_file())
    sql_cursor = conn.cursor()
    sql_cursor.execute("""
        CREATE TABLE if not exists "account" (
            "id"	INTEGER NOT NULL,
            "name"	TEXT,
            "def_amt"	INTEGER,
            "month"	INTEGER,
            "active"	INTEGER,
            "due_dom"	INTEGER,
            "note"	TEXT,
            PRIMARY KEY("id")
        )
    """)
    conn.commit()

    conn = sqlite3.connect(get_db_file())
    sql_cursor = conn.cursor()
    sql_cursor.execute("""
        CREATE TABLE if not exists "bill" (
            "account_id"	INTEGER NOT NULL,
            "amount"	INTEGER,
            "dt_paid"	INTEGER,
            "payment_confirmed" INTEGER,
            "note"	TEXT,
            "year"	INTEGER NOT NULL,
            "month"	INTEGER NOT NULL
        )
    """)
    conn.commit()

    # conn = sqlite3.connect(get_db_file())
    # sql_cursor = conn.cursor()
    # sql_cursor.execute("""
    #     INSERT INTO account (id, name, def_amt, active, due_dom, note)
    #     values (1, "account 1", 299, 1, 0, "")
    # """)
    # conn.commit()    