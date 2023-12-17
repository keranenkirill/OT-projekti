import tkinter as tk
from tkinter import messagebox
from views.view import View  # pylint: disable=import-error


class RegisterView(View):
    """
    View class for user registration in the Budget App.

    This class provides a user interface for registering a new account.
    It includes input fields for username, password, and repeat password.

    Attributes:
    - username (tk.Entry): Entry widget for entering the username.
    - password (tk.Entry): Entry widget for entering the password.
    - rpassword (tk.Entry): Entry widget for entering the repeated password.

    Methods:
    - __init__(self, parent, *args, **kwargs): Initializes the RegisterView instance.
    - widgets(self): Creates and configures the widgets for the registration view.
    - register_action(self): Handles the registration process when the button is clicked.
    - back_action(self): Navigates back to the login view.
    """

    def __init__(self, parent, *args, **kwargs):
        """
        Initializes the RegisterView instance.

        Args:
            parent: The parent widget.
            *args, **kwargs: Additional arguments and keyword arguments.
        """
        super().__init__(parent, bg="#1C2142", *args, **kwargs)
        self.pack(side=tk.LEFT, fill=tk.BOTH, pady=2, expand=True)
        self.widgets()

    def widgets(self):
        """
        Creates and configures the widgets for the registration view.
        """
        # Back button
        back_button = tk.Button(self, text="Back", command=self.back_action)
        back_button.pack(side=tk.TOP, anchor=tk.NW, padx=10, pady=10)

        registerform = View(self, bg="#1C2142")
        registerform.pack(side=tk.TOP, anchor=tk.CENTER)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # user
        usrlabel = tk.Label(registerform, text="Username:")
        usrentry = tk.Entry(registerform, width=50)

        usrlabel.grid(row=0, column=0, padx=10, pady=10)
        usrentry.grid(row=0, column=1, padx=10, pady=10)

        # password
        pwdlabel = tk.Label(registerform, text="Password:")
        pwdentry = tk.Entry(registerform, width=50, show="*")

        pwdlabel.grid(row=1, column=0, padx=10, pady=10)
        pwdentry.grid(row=1, column=1, padx=10, pady=10)

        # repeat password
        rpwdlabel = tk.Label(registerform, text="Repeat Password:")
        rpwdentry = tk.Entry(registerform, width=50, show="*")

        rpwdlabel.grid(row=2, column=0, padx=10, pady=10)
        rpwdentry.grid(row=2, column=1, padx=10, pady=10)

        btn_register_user = tk.Button(
            registerform, text="Register your account", command=self.register_action)
        btn_register_user.grid(row=3, column=1, padx=10, pady=10)

        self.username = usrentry
        self.password = pwdentry
        self.rpassword = rpwdentry

    def register_action(self):
        """
        Handles the registration process when the button is clicked.
        """
        print("registering....")
        u = self.username.get()
        p = self.password.get()
        rp = self.rpassword.get()

        if u and p and rp:
            if p == rp and u != "":
                if self.master.controller.register(u, p):
                    self.master.controller.load_login_view(account=u)
                else:
                    messagebox.showinfo("Registration Failed",
                     "Username already exists. Please choose a different username.")
            else:
                messagebox.showinfo("Check password",
                 "Passwords do not match. Please enter a valid password.")
        else:
            messagebox.showinfo("Error", "Please enter a valid username and password.")

    def back_action(self):
        """
        Navigates back to the login view.
        """
        self.master.controller.load_login_view()
