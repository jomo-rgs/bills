from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter
import calendar
from account import Account
from accounts import Accounts

from ctrl import Ctrl

def event_acct_selected(event: tkinter.Event):

    txtName['state'] = 'normal'
    txtDefault['state'] = 'normal'
    txtDOM['state'] = 'normal'
    txtNote['state'] = 'normal'
    dropActive['state'] = 'readonly'
    dropMonth['state'] = 'readonly'
    btnOk['state'] = 'normal'

    widget = event.widget
    account = accounts.get_account_at(widget.current())
    txtName.delete(0,END)
    txtName.insert(0,account.name)
    amt = int(account.def_amt) * .01
    txtDefault.delete(0,END)
    txtDefault.insert(0,"{:.2f}".format(amt))
    dropMonth.current(account.month)
    dropActive.current(account.active)
    txtDOM.delete(0,END)
    txtDOM.insert(0,account.due_dom)
    txtNote.delete(1.0,END)
    txtNote.insert(1.0, account.note if account.note != None else "")

    screen_root.update()



def event_click_ok():

    if mode == 1:                   # New
        account = Account(None)
        account.set_id(None) 
    else:                           # Edit
        account = accounts.get_selected_account()

    account.set_name(txtName.get().upper())

    # The amt is stored as a string with no decial. 
    t = txtDefault.get()
    if "." not in t:
        t = t + "00"
    elif "." in t:
        tt = t.split(".") 
        t = tt[0] + tt[1].rjust(2,'0')
    account.set_def_amt(t)
    #===============================================

    account.set_month(dropMonth.current())
    account.set_active(dropActive.current())
    account.set_due_dom(txtDOM.get())
    account.set_note(txtNote.get("1.0",END))

    account.save()
    
    screen_root.destroy()

def event_click_cancel():
    screen_root.destroy()


def account_form(p_mode: int):
    # Mode 1: New 2: Edit

    global mode, screen_root, accounts, query_accounts

    mode = p_mode

    width=230
    height=450
   
    screen_root = Tk()

    screen = Frame(screen_root) # width, height
    screen.grid(row=0, column=0,sticky=EW, columnspan=4) #padx, pady

    btn_frame = Frame(screen_root) # width, height
    btn_frame.grid(row=1, column=0,columnspan=4,padx=5,pady=5,sticky=NW) #padx, pady  
    
    Grid.rowconfigure(screen, 0, weight=1)
    Grid.columnconfigure(screen, 0, weight=1)
    Grid.rowconfigure(btn_frame, 0, weight=2)
    Grid.columnconfigure(btn_frame, 0, weight=2)    

    # Center window
    screen_width = screen.winfo_screenwidth()
    screen_height = screen.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)

    screen_root.geometry('%dx%d+%d+%d' % (width, height, x, y))
    screen_root.resizable(False,False)
    screen_root.title(f"Account")

    if mode == 2:
        accounts = Accounts(None, 'name')

        lblName = Label(screen, text="Account:")
        lblName.grid(row=0, column=0, sticky=NW, padx=10)
        query_accounts = [x.name for x in accounts.get_accounts()]
        dropAccounts = ttk.Combobox(screen, state="readonly", value=query_accounts)
        dropAccounts.grid(row=1, column=0, padx=10, sticky='NW')
        dropAccounts.bind("<<ComboboxSelected>>", event_acct_selected )

    # Name 
    global txtName
    lblName = Label(screen, text="Account Name:")
    lblName.grid(row=2, column=0, sticky=NW, padx=10)
    txtName = Entry(screen)
    txtName.grid(row=3, column=0, sticky=NW, padx=10)  

    # Default Value
    global txtDefault
    lblDefault = Label(screen, text="Default Amount:")
    lblDefault.grid(row=4, column=0, sticky=NW, padx=10)
    txtDefault = Entry(screen)
    txtDefault.grid(row=5, column=0, sticky=NW, padx=10)  

    # Month
    lblMonths = Label(screen, text="Months:")
    lblMonths.grid(row=6, column=0, sticky=W, padx=10)
    global dropMonth
    dropMonth = ttk.Combobox(screen, state="readonly")
    dropMonth['values'] = tuple(calendar.month_name)
    dropMonth.grid(row=7,column=0,sticky="W", padx=10)

    # Active
    lblActive = Label(screen, text="Active:")
    lblActive.grid(row=8, column=0, sticky=NW, padx=10)
    global dropActive
    dropActive = ttk.Combobox(screen, state="readonly", value=('No','Yes'))
    dropActive.grid(row=9,column=0,sticky="W", padx=10)
    dropActive.current(1)

    # Due Day of Month
    global txtDOM
    lblDOM = Label(screen, text="Day Due:")
    lblDOM.grid(row=10, column=0, sticky=W, padx=10)
    txtDOM = Entry(screen)
    txtDOM.grid(row=11, column=0, sticky=NW, padx=10)  

    # Note
    global txtNote
    lblNote = Label(screen, text="Note")
    lblNote.grid(row=12, column=0, sticky=NW, padx=10)
    txtNote = Text(screen, width=30, height=6)
    txtNote.grid(row=13, column=0,sticky=NW, padx=10, rowspan=1) 

    # txtNote.delete(1.0, END)
    # txtNote.insert(1.0, "nothing...")

    # Ok
    global btnOk
    btnOk = tkinter.Button(btn_frame, text ="Ok", command = event_click_ok)
    btnOk.grid(row=1,column=1, sticky=N)

    # Cancel
    global btnCancel
    btnCancel = tkinter.Button(btn_frame, text ="Cancel", command = event_click_cancel)
    btnCancel.grid(row=1,column=0, sticky=N)

    if mode == 2:
        txtName['state'] = 'disabled'
        txtDefault['state'] = 'disabled'
        txtDOM['state'] = 'disabled'
        txtNote['state'] = 'disabled'
        dropActive['state'] = 'disabled'
        dropMonth['state'] = 'disabled'
        btnOk['state'] = 'disabled'

    screen.mainloop()

    

#################################
#################################    
if __name__ == '__main__':
    # 1: New, 2: Edit
    account_form(2)