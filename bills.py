# Version 0.3 - Released Nov 16, 2022
# Version 0.4 - Released Dec 31, 2022
# Version 0.5 - Released Jan 13, 2023
# Version 0.6 - Released Jan 14, 2023
# Version 0.7 - Released Feb 22, 2023


from ast import Lambda
from re import MULTILINE
from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter
from tkinter.messagebox import showinfo
from tkinter import filedialog as fd
import account_form

from ctrl import Ctrl
import datetime

# Version 0.8 - Released on Feb 22, 2023

def bills():

    print("Start Bills...")
    version = "0.8.1"

    width=1080
    height=540
   
    bill_screen = Tk()

    # Center window
    screen_width = bill_screen.winfo_screenwidth()
    screen_height = bill_screen.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)

    bill_screen.geometry('%dx%d+%d+%d' % (width, height, x, y))
    bill_screen.resizable(False,False)
    bill_screen.title(f"Bills  v{version}")

    # Main Menu
    # bill_screen.option_add('*tearOff', FALSE)
    # win = Toplevel(bill_screen)
    # menubar = Menu(win)
    # menu_file = Menu(menubar)
    # menu_edit = Menu(menubar)
    # menubar.add_cascade(menu=menu_file, label='File')
    # menubar.add_cascade(menu=menu_edit, label='Edit')

    # menu_file.add_command(label='New')
    # menu_file.add_command(label='Open...')
    # menu_file.add_command(label='Close')

    # frame_menu = Frame(bill_screen) # width, height
    # frame_menu.grid(row=0, column=0,columnspan=4,padx=5,pady=5,sticky=NW) #padx, pady

    # menu = Menu(frame_menu)
    # frame_menu.config(menu=menu)
    
    # file_menu = Menu(menu)
    # file_menu.add_command(label='Exit')
    # menu.add_cascade(label='File', menu=file_menu)

    # edit_menu = Menu(menu)
    # edit_menu.add_command(label='Edit Accounts')
    # edit_menu.add_cascade(label='Add Account')
    # menu.add_cascade(label='Edit', menu=edit_menu)

    




    # # Parameter Frame
    frame_parameter = Frame(bill_screen) # width, height
    frame_parameter.grid(row=0, column=0,columnspan=4,padx=5,pady=5,sticky=NW) #padx, pady

    # Grid Frame
    frame_grid = Frame(bill_screen) # width, height
    frame_grid.grid(row=1, column=0,sticky=EW, columnspan=4) #padx, pady

    # Form Frame
    frame_form = Frame(bill_screen)
    frame_form.grid(row=2, column=0, sticky=NW, columnspan=4)

    # Strech when screen resize
    Grid.rowconfigure(bill_screen, 0, weight=1)
    Grid.columnconfigure(bill_screen, 0, weight=1)
    Grid.rowconfigure(frame_parameter, 0, weight=1)
    Grid.columnconfigure(frame_parameter, 0, weight=1)
    Grid.rowconfigure(frame_grid, 0, weight=1)
    Grid.columnconfigure(frame_grid, 0, weight=4)
    Grid.rowconfigure(frame_form, 1, weight=1)
    Grid.columnconfigure(frame_form, 1, weight=1)

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
        txtNote.delete('1.0',END)
        txtNote.insert('1.0',"")
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

            # print (record[0])
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
            txtAmountValue.set(bill_list[2])
            txtDatePaidValue.set(bill_list[3])
            txtNote.delete('1.0',END)
            txtNote['state'] = 'normal'
            txtNote.insert('1.0',bill_list[10])
            txtHiddenAccountId.set(bill_list[0])
            intPaymentConfirmed.set(bill_list[11])

    ###############################################################        
    def save_form():

        t = txtAmountValue.get()
        if "." not in t:
            t = t + "00"
        elif "." in t:
            tt = t.split(".") 
            t = tt[0] + tt[1].rjust(2,'0')
        #txtAmountValue.set(t)

        amt = int(t) * .01
        txtAmountValue.set( "{:.2f}".format(amt) )

        Ctrl.save_bill(dropYear.get(), dropMonth.get(), txtHiddenAccountId.get(), t, 
        txtNote.get('1.0',END), txtDatePaidValue.get(), intPaymentConfirmed.get())

        # Refresh grid values
        selected_item = tree.selection()[0]
        item = tree.item(selected_item)
        record = list(item['values'])
        record[2] = txtAmountValue.get()
        record[3] = txtDatePaidValue.get()
        record[4] = "Confirmed" if intPaymentConfirmed.get() == 1 else "" 
        record[10] = txtNote.get('1.0',END)



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

    ###############################################################
    def btnNewAccount_event():
        account_form.account_form(1)

    ###############################################################
    def btnEditAccount_event():
        account_form.account_form(2)
        
        


########################################################
## Main Screen
########################################################

    #####################################################################
    ## Dropdown Year
    #####################################################################
    dropYear = ttk.Combobox(frame_parameter, state="readonly", value=Ctrl.get_year_list())
    dropYear.current(0)
    dropYear.grid(row=0,column=0)
    # dropYear.pack()
    dropYear.bind("<<ComboboxSelected>>", loadMonth_event)

    #####################################################################
    ## Dropdown Month
    #####################################################################
    dropMonth = ttk.Combobox(frame_parameter,state="readonly", value=Ctrl.get_month_str_list())
    dropMonth.current(0)
    dropMonth.grid(row=0,column=1)
    # dropMonth.pack()
    dropMonth.bind("<<ComboboxSelected>>", loadMonth_event)

    #####################################################################
    ## Button Initilize Month
    #####################################################################
    btnInitilize = tkinter.Button(frame_parameter, text ="Initilize", command = btnInitilize_event)
    btnInitilize.grid(row=0,column=2)
    # btnInitilize.pack()

    #####################################################################
    ## Button New Account
    #####################################################################
    btnNewAccount = tkinter.Button(frame_parameter, text ="New Account", command = btnNewAccount_event)
    btnNewAccount.grid(row=0,column=3,sticky="NE")

    #####################################################################
    ## Button Edit Accounts
    #####################################################################
    btnEditAccount = tkinter.Button(frame_parameter, text ="Edit Accounts", command = btnEditAccount_event)
    btnEditAccount.grid(row=0,column=4,sticky="NE")


    #####################################################################
    ## Tree View
    #####################################################################
    global tree
    tree = ttk.Treeview(frame_grid)
    tree['columns'] = ("account_id","account","amount","date_paid","payment_confirmed","due_date","ytd","last_bill","last_year","note")

    tree.column("#0", width=0, stretch=NO)
    tree.column("account_id", width=0, stretch=NO) #Hidden
    tree.column("account", anchor=W, width=100)
    tree.column("amount", anchor=W, width=100)
    tree.column("date_paid", anchor=W, width=100)
    tree.column("payment_confirmed", anchor=W, width=100)
    tree.column("due_date", anchor=W, width=100)
    tree.column("ytd", anchor=W, width=50)
    tree.column("last_bill", anchor=W, width=50)
    tree.column("last_year", anchor=W, width=50)
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

    tree.grid(row=0, column=0, columnspan=1, sticky="EW")

    #####################################################################
    ## Form
    #####################################################################    

    global txtHiddenAccountId
    txtHiddenAccountId = tk.StringVar()

    # Amount 
    global txtAmountValue, txtAmount
    txtAmountValue = tk.StringVar()
    lblAmount = Label(frame_form, text="Amount")
    lblAmount.grid(row=0, column=0, sticky=NW)
    txtAmount = Entry(frame_form, textvariable=txtAmountValue)
    # amount_txt.set("9.99")
    txtAmount.grid(row=1, column=0, sticky=NW)  

    # Date Paid
    global txtDatePaidValue, txtDatePaid
    txtDatePaidValue = tk.StringVar()
    lblDatePaid = Label(frame_form, text="Date Paid")
    lblDatePaid.grid(row=2, column=0, sticky=NW)
    txtDatePaid = Entry(frame_form, textvariable=txtDatePaidValue)
    txtDatePaid.grid(row=3, column=0,sticky=NW)  

    # Today
    global btnToday
    btnToday = tkinter.Button(frame_form, text ="Today", command = set_today)
    btnToday.grid(row=4, column=0, sticky=NW)     

    # Note
    global txtNote
    lblNote = Label(frame_form, text="Note")
    lblNote.grid(row=0, column=2, sticky=NW, padx=10)
    txtNote = Text(frame_form, width=112, height=8)
    txtNote.grid(row=1, column=2,sticky=NW, padx=10, rowspan=4) 

    # Payment Confirmed 
    global intPaymentConfirmed, chkPaymentConfirmed
    intPaymentConfirmed = tk.IntVar()
    chkPaymentConfirmed = Checkbutton(frame_form, variable=intPaymentConfirmed, text="Payment Confirmed", onvalue=1, offvalue=0 )
    chkPaymentConfirmed.grid(row=5,column=0, pady=10, padx=5, sticky=W) 

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