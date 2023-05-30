from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter
import calendar
from account import Account
from accounts import Accounts

from ctrl import Ctrl

def event_click_ok():
    account = Account(None)
    account.set_id(None) 
    account.set_name(txtNameValue.get())

    # The amt is stored as a string with no decial. 
    t = txtDefaultlValue.get()
    if "." not in t:
        t = t + "00"
    elif "." in t:
        tt = t.split(".") 
        t = tt[0] + tt[1].rjust(2,'0')
    account.set_def_amt(t)
    #===============================================

    account.set_month(dropMonth.current())
    account.set_active(dropMonth.current())
    account.set_due_dom(txtDOMValue.get())
    account.set_note(txtNote.get("1.0",END))

    account.save()
    
    screen.destroy()

def event_click_cancel():
    screen.destroy()


def account_form(mode: int):

    global screen, selected_account
    screen = Tk()
    accounts = Accounts()
    
    if mode != 1:
        lblName = Label(screen, text="Account:")
        lblName.grid(row=0, column=0, sticky=NW)
        # dropAccounts = ttk.Combobox(screen, state="readonly", value=ct.get_account_list())
        dropAccounts = ttk.Combobox(screen, state="readonly", value=accounts.get_all_accounts())
        dropAccounts.grid(row=0, column=0, padx=100, sticky='NW')

    # Name 
    global txtNameValue, txtName
    txtNameValue = tk.StringVar()
    # txtNameValue.set(selected_account.name)
    lblName = Label(screen, text="Account Name:")
    lblName.grid(row=1, column=0, sticky=NW)
    txtName = Entry(screen, textvariable=txtNameValue)
    txtName.grid(row=2, column=0, sticky=NW)  

    # Default Value
    global txtDefaultlValue, txtDefault
    txtDefaultlValue = tk.StringVar()
    # txtDefaultlValue.set(selected_account.def_amt)
    lblDefault = Label(screen, text="Default Amount:")
    lblDefault.grid(row=3, column=0, sticky=NW)
    txtDefault = Entry(screen, textvariable=txtDefaultlValue)
    txtDefault.grid(row=4, column=0, sticky=NW)  

    # Month
    lblMonths = Label(screen, text="Months:")
    lblMonths.grid(row=5, column=0, sticky=W)
    global dropMonth
    dropMonth = ttk.Combobox(screen, state="readonly")
    dropMonth['values'] = tuple(calendar.month_name)
    dropMonth.grid(row=6,column=0,sticky="W")

    # Active
    lblActive = Label(screen, text="Active:")
    lblActive.grid(row=7, column=0, sticky=NW)
    dropActive = ttk.Combobox(screen, state="readonly", value=('No','Yes'))
    dropActive.grid(row=8,column=0,sticky="W")
    dropActive.current(1)

    # Due Day of Month
    global txtDOMValue, txtDOM
    txtDOMValue = tk.StringVar()
    # txtDOMValue.set(selected_account.due_dom)
    lblDOM = Label(screen, text="Day Due:")
    lblDOM.grid(row=9, column=0, sticky=W)
    txtDOM = Entry(screen, textvariable=txtDOMValue)
    txtDOM.grid(row=10, column=0, sticky=NW)  

    # Note
    global txtNote
    lblNote = Label(screen, text="Note")
    lblNote.grid(row=11, column=0, sticky=NW, padx=10)
    txtNote = Text(screen, width=80, height=8)
    txtNote.grid(row=12, column=0,sticky=NW, padx=10, rowspan=4) 

    # Ok
    btnOk = tkinter.Button(screen, text ="Ok", command = event_click_ok)
    btnOk.grid(row=16,column=0, sticky=NE)

    # Cancel
    btnOk = tkinter.Button(screen, text ="Cancel", command = event_click_cancel)
    btnOk.grid(row=16,column=1, sticky=NE)

    if mode == 1:
        pass
    else:
        pass

        #     dropAccountsValues = list()
        # for item in accounts.get_all_accounts():
        #     dropAccountsValues.append(item.name)

    screen.mainloop()

    

#################################
#################################    
if __name__ == '__main__':
    account_form(1)