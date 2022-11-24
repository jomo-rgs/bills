from tkinter import *
from tkinter import ttk
import tkinter as tk
import tkinter

from ctrl import Ctrl


def accounts():
    screen = Tk()

    dropAccounts = ttk.Combobox(screen, state="readonly", value=Ctrl.get_account_list())
    # dropAccounts.current(0)
    dropAccounts.grid(row=0,column=0)

    screen.mainloop()

#################################
#################################    
if __name__ == '__main__':
    accounts()