import tkinter as tk
from tkinter import ttk


class View(tk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.style = ttk.Style(self)
        
    def remove(self):
        self.pack_forget()
