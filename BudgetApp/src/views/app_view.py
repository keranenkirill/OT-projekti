import tkinter as tk
from views.view_controller import ViewController  # pylint: disable=import-error

class UserConfig():
    def __init__(self):
        self.user_id = 0
        self.username = 0

    def set_auth(self, username, usrid):
        self.user_id = usrid
        self.username = username

class Application(tk.Tk):
    def __init__(self, title, width=800, height=600):
        super().__init__()
        self.minsize(1000, 600)
        self.title(title)
        self.geometry(f'{width}x{height}')
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.protocol("WM_SLEEP", self.on_close)

        self.config = UserConfig()
        self.controller = ViewController(self)

    def on_close(self):
        self.quit()

    def run(self):
        self.mainloop()
