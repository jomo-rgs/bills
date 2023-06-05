import tkinter as tk
import sqlite3
import services
import re

###########################
## CLASS ACCOUNT
###########################
class Account:

    #########################
    # CONSTRUCTOR
    #########################
    def __init__(self, account: tuple):
        self.id = None 
        self.name = ''
        self.def_amt = 0.00
        self.month = 0
        self.active = 0
        self.due_dom = 0
        self.note = ''

        if account != None:
            self.set_id(account[0])
            self.set_name(account[1])
            self.set_def_amt(account[2])
            self.set_month(account[3])
            self.set_active(account[4])
            self.set_due_dom(account[5])
            self.set_note(account[6])

    # Setters. Not using Getters.
    def set_id(self, x):
        self.id = x        

    def set_name(self, x):
        self.name = x.strip()
        if len(self.name) < 1:
            self.name = "<blank>"

    def set_def_amt(self, x: str):
        if isinstance(x,str):
            x = re.sub("[^0-9]", "", x)
            
        self.def_amt = abs(float(x))

    def set_month(self, x: int):
        if x != None:
            self.month = int(x)

    def set_active(self, x: int):
        if x != None:
            self.active = int(x)

    def set_due_dom(self, x: str):
        if isinstance(x, str):
            x = re.sub("[^0-9]", "", x)

        self.due_dom = int(x)

    def set_note(self, x):
        self.note = x
        

    ###############################
    ## SAVE
    ###############################
    def save(self):              

        data = Data()

        if self.id == None:
            data.insert(self)   
        else: 
            data.update(self) 


    ###############################
    ## TO_STRING
    ###############################
    def to_string(self):
        return f"id: {self.id}\n name: {self.name}\n def_amt: {self.def_amt}\n month:{self.month}\n active: {self.active}\n due_dom: {self.due_dom}\n note: {self.note}"

    
############################
## CLASS DATA
############################
class Data:

    ###########################
    ## INSERT
    ###########################
    def insert(self, acccount: Account):
        sql = """
        insert into account (id, name, def_amt, month, active, due_dom, note)
        values (:id, :name, :def_amt, :month, :active, :due_dom, :note);
        """
        self.exe(sql, acccount)

    ###########################
    ## UPDATE
    ###########################
    def update(self, account: Account):
        sql = """
        update account
        set name = :name, 
        def_amt = :def_amt, 
        month = :month, 
        active = :active, 
        due_dom = :due_dom, 
        note = :note  
        where id = :id;
        """  
        self.exe(sql, account)

    ###########################
    ## EXE
    ###########################
    def exe(self, sql: str, account: Account):        
        conn = sqlite3.connect(services.get_db_file())
        sql_cursor = conn.cursor()
        sql_cursor.execute(sql,
        {
            'id':account.id, 
            'name':account.name, 
            'def_amt':account.def_amt, 
            'month':account.month, 
            'active':account.active, 
            'due_dom':account.due_dom, 
            'note':account.note            
        })

        conn.commit()
        conn.close() 