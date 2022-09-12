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
        insert into bill (amount, account_id,year,month)
        select def_amt, id,:year,:month
        from account
        where (month is null or  month = :month)
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
    # due_date2, account_id, note are hiddent in treeview 
    # due_date2 is only used for order, Be sure to leave it at the end of sql
    # strftime('%m/%d/%Y',bill.dt_paid)
    conn = sqlite3.connect(get_db_file())
    sql_cursor = conn.cursor()
    sql_cursor.execute("""
        select account.id, account.name, bill.amount, strftime('%Y-%m-%d',bill.dt_paid) dt_paid,  
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

#####################################################
#####################################################    
def save_bill(year, month, account_id, amount, note, dt_paid):
    conn = sqlite3.connect(get_db_file())
    sql_cursor = conn.cursor()
    sql_cursor.execute("""
        update bill
            set amount =  :amount,
                note = :note,
                dt_paid = date(dt_paid)
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
        'dt_paid':dt_paid
    })

    conn.commit()
    conn.close() 