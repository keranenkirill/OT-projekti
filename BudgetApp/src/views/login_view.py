import tkinter as tk
from tkinter import messagebox
from views.view import View  # pylint: disable=import-error


class LoginView(View):
    """
    View class for user login in the Budget App.

    This class provides a user interface for logging into the application.
    It includes input fields for username and password, along with options
    for revealing the password, registering a new account, and logging in.

    Attributes:
    - username (tk.Entry): Entry widget for entering the username.
    - password (tk.Entry): Entry widget for entering the password.
    - revealvar (tk.BooleanVar): Boolean variable for controlling password visibility.

    Methods:
    - __init__(self, parent, *args, account="", **kwargs): Initializes the LoginView instance.
    - widgets(self): Creates and configures the widgets for the login view.
    - reveal_actions(self): Handles actions related to revealing or hiding the password.
    - login_action(self): Handles the login process when the Login button is clicked.
    - register_action(self): Navigates to the registration view when the Register button is clicked.
    """

    def __init__(self, parent, *args, account="", **kwargs):
        """
        Initializes the LoginView instance.

        Args:
            parent: The parent widget.
            *args, **kwargs: Additional arguments and keyword arguments.
            account (str): The default account (username) to pre-fill in the login form.
        """
        super().__init__(parent, *args, **kwargs,  bg="#49183A")
        self.account = account
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.widgets()

    def widgets(self):  # pylint: disable=too-many-statements
        """
        Creates and configures the widgets for the login view.
        """
        loginform = View(self, bg="#49183A")
        loginform.pack(side=tk.TOP, anchor=tk.CENTER, padx=10, pady=50)

        # user
        usrlabel = tk.Label(loginform, text="Username:")
        usrentry = tk.Entry(loginform, width=50)

        usrlabel.grid(row=0, column=0, padx=10, pady=10)
        usrentry.grid(row=0, column=1, padx=10, pady=10)

        # password
        pwdlabel = tk.Label(loginform, text="Password:")
        pwdentry = tk.Entry(loginform, width=50, show="*")

        pwdlabel.grid(row=1, column=0, padx=10, pady=10)
        pwdentry.grid(row=1, column=1, padx=10, pady=10)

        self.revealvar = tk.BooleanVar()
        reveal = tk.Checkbutton(loginform, var=self.revealvar,
                                text="reveal password", command=self.reveal_actions)
        reveal.grid(row=2, column=0, padx=10, pady=10)

        btn_register_user = tk.Button(
            master=loginform, text="No Account? Register here.", command=self.register_action)
        btn_register_user.grid(row=3, column=1, padx=10, pady=10)

        btn_login_user = tk.Button(
            master=loginform, text="Login", command=self.login_action)
        btn_login_user.grid(row=3, column=2, columnspan=1, padx=10, pady=10)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.username = usrentry
        self.password = pwdentry

        self.username.insert(0, self.account)
        self.pack(side=tk.LEFT, fill=tk.BOTH, pady=2, expand=True)

    def reveal_actions(self):
        """
        Handles actions related to revealing or hiding the password.
        """
        if self.revealvar.get():
            self.password.config(show="")
        else:
            self.password.config(show="*")

    def login_action(self):
        """
        Handles the login process when the Login button is clicked.
        """
        username = self.username.get()
        password = self.password.get()

        if username and password:
            user_id = self.master.controller.login(username, password)
            if user_id is not None:
                self.master.config.set_auth(username, user_id)
                self.master.controller.load_budget_view()
            else:
                messagebox.showinfo(
                    "Login Error", "Invalid username or password. Please try again.")
        else:
            messagebox.showinfo(
                "Login Error", "Please enter both username and password.")

    def register_action(self):
        """
        Navigates to the registration view when the Register button is clicked.
        """
        self.master.controller.load_register_view()
