import tkinter as tk
from views.view_controller import ViewController  # pylint: disable=import-error

class UserConfig():
    """
    Configuration class to store user-related information.

    Attributes:
    - user_id (int): The user ID.
    - username (str): The username.

    Methods:
    - set_auth(self, username, user_id): Sets the user authentication information.
    """
    def __init__(self):
        """
        Initializes the UserConfig instance with default values.
        """
        self.user_id = 0
        self.username = 0

    def set_auth(self, username, usrid):
        """
        Sets the user authentication information.

        Args:
            username (str): The username.
            user_id (int): The user ID.
        """
        self.user_id = usrid
        self.username = username

class Application(tk.Tk):
    """
    Main application class for the Budget App.

    This class represents the main window of the application and manages the user interface.

    Attributes:
    - config (UserConfig): An instance of the UserConfig class to store user-related information.
    - controller (ViewController): An instance of the ViewController class to handle application logic.

    Methods:
    - __init__(self, title, width=800, height=600): Initializes the Application instance.
    - on_close(self): Handles the window close event.
    - run(self): Starts the application main loop.
    """
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
        """
        Handles the window close event.
        """
        self.quit()

    def run(self):
        """
        Starts the application main loop.
        """
        self.mainloop()
