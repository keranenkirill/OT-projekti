import tkinter as tk
from tkinter import ttk


class View(tk.Frame):
    """
    Base class for creating views in a tkinter-based application.

    This class extends the tkinter Frame class and provides a basic structure for creating views.
    It includes a ttk.Style instance for styling and provides a 'remove' method to hide the view.

    Attributes:
    - style (ttk.Style): The ttk.Style instance associated with the view.

    Methods:
    - __init__(self, parent, *args, **kwargs): Initializes the View instance.
    - remove(self): Hides the view by using the 'pack_forget' method.
    """
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.style = ttk.Style(self)
    def remove(self):
        self.pack_forget()
