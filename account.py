import tkinter as tk

class Account:

    def __init__(self, account: tuple):
        self.id, self.name, self.def_amt, self.month, self.active, self.due_dom, self.note = account


class Data:

    def __init__(self):
        pass