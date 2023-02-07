# Version 0.3 - Released Nov 16, 2022
# Version 0.4 - Released Dec 31, 2022
# Version 0.5 - Released Jan 13, 2023
# Version 0.6 - Released Jan 14, 2023


from ast import Lambda
from re import MULTILINE
from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter
from tkinter.messagebox import showinfo
from tkinter import filedialog as fd

from ctrl import Ctrl
import datetime

def bills():

    print("Start Bills...")
    version = 0.6

    bill_screen = Tk()
    bill_screen.title(f"Bills  v{version}")

    Ctrl.init_db()

    ############################################################
    def btnInitilize_event():

        # Populate database with values
        Ctrl.initilize_month(dropYear.get(),dropMonth.get())

        loadMonth_event(None)

    ############################################################
    def loadMonth_event(e):

        #Clear the treeview list items
        for item in tree.get_children():
            tree.delete(item)

        #Update Grid
        bills = Ctrl.get_bill_list(dropYear.get(),dropMonth.get())
        for bill in bills:
            # print(bill)
            # tree.insert(parent="", index="end", values=("CCU 540 Power 2", "150.00", "8/22/2022", "27th", "5000", "175.00"))
            bill = list(bill)
            bill[2] = f"{bill[2]/100:.2f}"                  # amount
            bill[4] = "Confirmed" if bill[11] == 1 else ""  # payment_confirmed
            bill[6] = f"{bill[6]/100:.2f}"                  # ytd
            tree.insert(parent="", index="end", values=bill)

        #Clear Form Values
        txtAmountValue.set("")
        txtDatePaidValue.set("")
        txtNoteValue.set("")
        txtHiddenAccountId.set("")
        intPaymentConfirmed.set(0)

        # Lock form from input
        txtAmount.config(state= "disabled")
        txtDatePaid.config(state= "disabled")
        txtNote.config(state= "disabled")
        chkPaymentConfirmed.config(state= "disabled")
        btnViewDocs.config(state= "disabled")
        btnAttachDocs.config(state= "disabled")
        btnSave.config(state= "disabled")

        # Update Status Bar at bottom
        p_year = dropYear.get()
        p_account = ''
        p_amt = Ctrl.get_ytd(p_year, p_account)
        lblYtdValue.set(p_amt)

        p_month = dropMonth.get()
        p_amt = Ctrl.get_month_total(p_month)
        lblMonthTotalValue.set(p_amt)
        


    ###############################################################
    def tree_select(event):
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item['values']

            print (record[0])
            populate_form(record)

            # Lock form from input
            txtAmount.config(state= "normal")
            txtDatePaid.config(state= "normal")
            txtNote.config(state= "normal")
            chkPaymentConfirmed.config(state= "normal")
            btnViewDocs.config(state= "normal")
            btnAttachDocs.config(state= "normal")
            btnSave.config(state= "normal")

    ###############################################################
    def populate_form(bill_list):
            # lblAmount[] = bill_lis[2]
            txtAmountValue.set(bill_list[2])
            txtDatePaidValue.set(bill_list[3])
            txtNoteValue.set(bill_list[10])
            txtHiddenAccountId.set(bill_list[0])
            intPaymentConfirmed.set(bill_list[11])

    ###############################################################        
    def save_form():
        Ctrl.save_bill(dropYear.get(), dropMonth.get(), txtHiddenAccountId.get(), txtAmountValue.get(), 
        txtNoteValue.get(), txtDatePaidValue.get(), intPaymentConfirmed.get())

        # Refresh grid values
        selected_item = tree.selection()[0]
        item = tree.item(selected_item)
        record = list(item['values'])
        record[2] = txtAmountValue.get()
        record[3] = txtDatePaidValue.get()
        record[4] = "Confirmed" if intPaymentConfirmed.get() == 1 else "" 
        record[10] = txtNoteValue.get()

        tree.item(selected_item, text="", values=record)
        # for selected_item in tree.selection():
        #     item = tree.item(selected_item)
        #     record = item['values']

    ###############################################################        
    def set_today(): 
        dt = datetime.datetime.now()
        month = dt.strftime("%m")
        day = dt.strftime("%d")
        year = dt.strftime("%Y")
        txtDatePaidValue.set(f"{year}-{month}-{day}")
        
        


    ###############################################################
    def btnAttachDocs_click():
        fileToOpen = fd.askopenfilename()
        if isinstance(fileToOpen, str):
            Ctrl.attachDoc(fileToOpen, txtHiddenAccountId.get(), dropYear.get(), dropMonth.get())

    ###############################################################
    def btnViewDocs_click():
        Ctrl.viewDocs(txtHiddenAccountId.get(), dropYear.get(), dropMonth.get())

    #####################################################################
    ## Dropdown Year
    #####################################################################
    dropYear = ttk.Combobox(bill_screen, state="readonly", value=Ctrl.get_year_list())
    dropYear.current(0)
    dropYear.grid(row=0,column=0,pady=20, padx=25, sticky=W)
    dropYear.bind("<<ComboboxSelected>>", loadMonth_event)

    #####################################################################
    ## Dropdown Month
    #####################################################################
    dropMonth = ttk.Combobox(bill_screen,state="readonly", value=Ctrl.get_month_str_list())
    dropMonth.current(0)
    dropMonth.grid(row=0,column=0,pady=20, padx=215, sticky=W)
    dropMonth.bind("<<ComboboxSelected>>", loadMonth_event)


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
    tree['columns'] = ("account_id","account","amount","date_paid","payment_confirmed","due_date","ytd","last_bill","last_year","note")

    tree.column("#0", width=0, stretch=NO)
    tree.column("account_id", width=0, stretch=NO) #Hidden
    tree.column("account", anchor=W, width=120)
    tree.column("amount", anchor=W, width=120)
    tree.column("date_paid", anchor=W, width=120)
    tree.column("payment_confirmed", anchor=W, width=155)
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
    tree.heading("payment_confirmed", text="Payment Confirmed", anchor=CENTER)
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
    global txtAmountValue, txtAmount
    txtAmountValue = tk.StringVar()
    lblAmount = Label(bill_screen, text="Amount")
    lblAmount.grid(row=3, column=0, sticky=W, padx=5)
    txtAmount = Entry(bill_screen, textvariable=txtAmountValue)
    # amount_txt.set("9.99")
    txtAmount.grid(row=4, column=0,sticky=W, padx=5)

    # Note
    global txtNoteValue, txtNote
    txtNoteValue = tk.StringVar()
    lblNote = Label(bill_screen, text="Note")
    lblNote.grid(row=3, column=1, sticky=W, padx=5)
    txtNote = Entry(bill_screen,textvariable=txtNoteValue)
    txtNote.grid(row=4, column=1,sticky=W, padx=5, columnspan=2)

    # Date Paid
    global txtDatePaidValue, txtDatePaid
    txtDatePaidValue = tk.StringVar()
    lblDatePaid = Label(bill_screen, text="Date Paid")
    lblDatePaid.grid(row=5, column=0, sticky=W, padx=5)
    txtDatePaid = Entry(bill_screen, textvariable=txtDatePaidValue)
    txtDatePaid.grid(row=6, column=0,sticky=W, padx=5)  

    # Today
    global btnToday
    btnToday = tkinter.Button(bill_screen, text ="Today", command = set_today)
    btnToday.grid(row=6,column=0, pady=10, padx=180, sticky=W)     

    # Payment Confirmed 
    global intPaymentConfirmed, chkPaymentConfirmed
    intPaymentConfirmed = tk.IntVar()
    chkPaymentConfirmed = Checkbutton(bill_screen, variable=intPaymentConfirmed, text="Payment Confirmed", onvalue=1, offvalue=0 )
    chkPaymentConfirmed.grid(row=8,column=0, pady=10, padx=5, sticky=W) 

    # Save
    global btnSave
    btnSave = tkinter.Button(bill_screen, text ="Save", command = save_form)
    btnSave.grid(row=9,column=0, pady=20, padx=5, sticky=W)     

    # View Documents
    global btnViewDocs
    btnViewDocs = tkinter.Button(bill_screen, text ="View Documents", command = btnViewDocs_click)
    btnViewDocs.grid(row=9,column=0, pady=20, padx=70, sticky=W) 

    # Attach Documents
    global btnAttachDocs
    btnAttachDocs = tkinter.Button(bill_screen, text ="Attach Document", command = btnAttachDocs_click)
    btnAttachDocs.grid(row=9,column=0, pady=20, padx=215, sticky=W) 

    # Seperator Line
    seperator = ttk.Separator(bill_screen, orient='horizontal')
    seperator.grid(row=10,sticky="ew",columnspan=4)

    # YTD
    global lblYtdValue
    lblYtdValue = tk.StringVar()
    lblYtd = Label(bill_screen, textvariable=lblYtdValue)
    lblYtd.grid(row=11, column=0, sticky=W, padx=5)

    # Month Total
    global lblMonthTotalValue
    lblMonthTotalValue = tk.StringVar()
    lblMonthTotal = Label(bill_screen, textvariable=lblMonthTotalValue)
    lblMonthTotal.grid(row=11, column=0, sticky=W, padx=150)

    # DB Path
    global lblDbPathValue
    lblDbPathValue = tk.StringVar()
    lblDbPathValue.set(Ctrl.get_db_path())
    blDbPath = Label(bill_screen, textvariable=lblDbPathValue)
    blDbPath.grid(row=11, column=3, sticky=E)    

    loadMonth_event(None)

    bill_screen.mainloop()



#################################
#################################    
if __name__ == '__main__':
    bills()