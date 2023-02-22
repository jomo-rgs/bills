import os
import sys
from ast import Pass
import datetime
import data
import shutil
import subprocess
from tkinter import filedialog

class Ctrl():

    def init_db():
        data.create_db()

        print(f"Platform: {sys.platform}")

    def get_month_str_list():
        months_choices = []
        for i in range(1,13):
            months_choices.append(datetime.date(datetime.date.today().year, i, 1).strftime('%B'))

        return months_choices
    
    def get_db_path():
        return data.get_db_file()    

    def get_year_list():
        years_choices = []
        for ii in range(2022,datetime.date.today().year + 1):
            years_choices.append(ii)

        return years_choices
    
    def get_account_list():
        return data.query_distinct_account_name()

    def initilize_month(intYear, strMonth):
        strMonthList = Ctrl.get_month_str_list()
        data.initilize_month_sql(intYear, strMonthList.index(strMonth)+1)

    def get_bill_list(intYear, strMonth):
        strMonthList = Ctrl.get_month_str_list()
        return data.get_bill_list(intYear, strMonthList.index(strMonth)+1)

    def get_bill(year, month, account):
        pass

    def save_bill(intYear, strMonth, account_id, amount, note, dt_paid, payment_confirmed):
        strMonthList = Ctrl.get_month_str_list()
        data.save_bill(intYear, strMonthList.index(strMonth)+1, account_id, amount.replace(".",""), note, dt_paid, payment_confirmed)

    def viewDocs():
        pass

    def attachDoc(docToAttach, accountId, year, month):
        print(f"Doc to attach: {docToAttach} {len(docToAttach)}")

        if len(docToAttach) >= 0:

            docs_path = f"{accountId}{year}{month}"
            # docs_path = os.path.join("./docs",docs_path)
            docs_path = os.path.join(os.getcwd(),"docs",docs_path)

            # Create dir if needed
            print("Does it exist???")
            if not os.path.exists(docs_path):
                print(f"Path does not exist: {docs_path}")
                os.makedirs(docs_path)

            # Copy file to directory if not already there.
            new_file = os.path.join(docs_path, os.path.basename(docToAttach))
            if not os.path.exists(new_file):
                shutil.copyfile(docToAttach, new_file)

    def viewDocs(accountId, year, month):
        docs_path = f"{accountId}{year}{month}"
        # docs_path = os.path.join("./docs",docs_path)
        docs_path = os.path.join(os.getcwd(),"docs",docs_path)

        # Create dir if needed
        print("Does it exist???")
        if not os.path.exists(docs_path):
            print(f"Path does not exist: {docs_path}")
            os.makedirs(docs_path)        

        # filedialog.askopenfilename(title = "Select a File",
        #                                   filetypes = (("all files","*.*")) )
        if os.path.exists(docs_path):
            # Linux
            if sys.platform == "linux":
                os.system(f"xdg-open {docs_path}")
            print(os.name)
            # mac
            if sys.platform == "darwin":
                docs_path = docs_path + "/"
                subprocess.call(["open", docs_path])
            # windows
            if sys.platform == "win32":
                subprocess.Popen(f"explorer /select,{docs_path}")

    def get_ytd(year, account):
        num = data.get_ytd(year, account)[0]
        return f'YTD: ${num:,.2f}' if num != None else "0.00"
    
    def get_month_total(month):  
        strMonthList = Ctrl.get_month_str_list()
        intMonth = int(strMonthList.index(month)+1)  
        num = data.get_month_total(intMonth)[0]
        return f'Month Total: ${num:,.2f}' if num != None else "0.00"

    # def get_month_list():
    #     months_choices = []
    #     for i in range(1,13):
    #         months_choices.append(datetime.date(datetime.date.today().year, i, 1).strftime('%B'))

    #     return months_choices

    # def get_year_list():
    #     years_choices = []
    #     for ii in range(1,13):
    #         years_choices.append((datetime.date.today().year -10) + ii)

    #     return years_choices

