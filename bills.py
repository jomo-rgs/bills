from ast import Lambda
from re import MULTILINE
from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter
from tkinter.messagebox import showinfo

from ctrl import Ctrl

def bills():

    print("Start Bills...")

    bill_screen = Tk()

    ############################################################
    def btnInitilize_event():

        # Populate database with values
        Ctrl.initilize_month(dropYear.get(),dropMonth.get())

        #Clear the treeview list items
        for item in tree.get_children():
            tree.delete(item)

        #Update Grid
        bills = Ctrl.get_bill_list(dropYear.get(),dropMonth.get())
        for bill in bills:
            print(bill)
            # tree.insert(parent="", index="end", values=("CCU 540 Power 2", "150.00", "8/22/2022", "27th", "5000", "175.00"))
            tree.insert(parent="", index="end", values=bill)

    ###############################################################
    def tree_select(event):
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item['values']

            print (record[0])
            populate_form(record)

    ###############################################################
    def populate_form(bill_list):
            # lblAmount[] = bill_lis[2]
            txtAmountValue.set(bill_list[2])
            txtDatePaidValue.set(bill_list[3])
            txtNoteValue.set(bill_list[9])
            txtHiddenAccountId.set(bill_list[0])
        
    def save_form():
        Ctrl.save_bill(dropYear.get(),dropMonth.get(), txtHiddenAccountId.get(), txtAmountValue.get(), txtNoteValue.get(), txtDatePaidValue.get())
        


    #####################################################################
    ## Dropdown Year
    #####################################################################
    dropYear = ttk.Combobox(bill_screen, value=Ctrl.get_year_list())
    dropYear.current(0)
    dropYear.grid(row=0,column=0)

    #####################################################################
    ## Dropdown Month
    #####################################################################
    dropMonth = ttk.Combobox(bill_screen,value=Ctrl.get_month_str_list())
    dropMonth.current(0)
    dropMonth.grid(row=0,column=1)

    #####################################################################
    ## Button Initilize Month
    #####################################################################
    btnInitilize = tkinter.Button(bill_screen, text ="Initilize", command = btnInitilize_event)
    btnInitilize.grid(row=0,column=3)

    #####################################################################
    ## Tree View
    #####################################################################
    global tree
    tree = ttk.Treeview(bill_screen)
    tree['columns'] = ("account_id","account","amount","date_paid","due_date","ytd","last_bill","last_year","note")

    tree.column("#0", width=0, stretch=NO)
    tree.column("account_id", width=0, stretch=NO) #Hidden
    tree.column("account", anchor=W, width=120)
    tree.column("amount", anchor=W, width=120)
    tree.column("date_paid", anchor=W, width=120)
    tree.column("due_date", anchor=W, width=120)
    tree.column("ytd", anchor=W, width=120)
    tree.column("last_bill", anchor=W, width=120)
    tree.column("last_year", anchor=W, width=120)
    tree.column("note", width=0, stretch=NO) #Hidden

    tree.heading("#0", text="", anchor=CENTER)
    tree.heading("account_id", text="Account ID") #Hidden
    tree.heading("account", text="Account", anchor=CENTER)
    tree.heading("amount", text="Amount", anchor=CENTER)
    tree.heading("date_paid", text="Date Paid", anchor=CENTER)
    tree.heading("due_date", text="Due Date", anchor=CENTER)
    tree.heading("ytd", text="YTD", anchor=CENTER)
    tree.heading("last_bill", text="Last Bill", anchor=CENTER)
    tree.heading("last_year", text="Last Year", anchor=CENTER)
    tree.heading("note", text="Last Year", anchor=CENTER)

    tree.bind('<<TreeviewSelect>>', tree_select)

    tree.grid(row=2, column=0, columnspan=4, pady=5)

    #####################################################################
    ## Form
    #####################################################################    

    global txtHiddenAccountId
    txtHiddenAccountId = tk.StringVar()

    # Amount 
    global txtAmountValue
    txtAmountValue = tk.StringVar()
    lblAmount = Label(bill_screen, text="Amount")
    lblAmount.grid(row=3, column=0, sticky=W, padx=5)
    txtAmount = Entry(bill_screen, textvariable=txtAmountValue)
    # amount_txt.set("9.99")
    txtAmount.grid(row=4, column=0,sticky=W, padx=5)

    # Note
    global txtNoteValue
    txtNoteValue = tk.StringVar()
    lblNote = Label(bill_screen, text="Note")
    lblNote.grid(row=3, column=1, sticky=W, padx=5)
    txtNote = Entry(bill_screen,textvariable=txtNoteValue)
    txtNote.grid(row=4, column=1,sticky=W, padx=5, columnspan=2)

    # Date Paid
    global txtDatePaidValue
    txtDatePaidValue = tk.StringVar()
    lblDatePaid = Label(bill_screen, text="Date Paid")
    lblDatePaid.grid(row=5, column=0, sticky=W, padx=5)
    txtDatePaid = Entry(bill_screen, textvariable=txtDatePaidValue)
    txtDatePaid.grid(row=6, column=0,sticky=W, padx=5)  

    # Files
    btnFiles = tkinter.Button(bill_screen, text ="Files", command = Ctrl.initilize_month)
    btnFiles.grid(row=7,column=0, pady=10, padx=5, sticky=E) 

    # Save
    btnSave = tkinter.Button(bill_screen, text ="Save", command = save_form)
    btnSave.grid(row=7,column=1, pady=10, padx=5, sticky=W) 

    bill_screen.mainloop()


#################################
#################################    
if __name__ == '__main__':
    bills()