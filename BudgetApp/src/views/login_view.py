import tkinter as tk
from tkinter import messagebox
from views.view import View  # pylint: disable=import-error


class LoginView(View):

    def __init__(self, parent, *args, account="", **kwargs):
        super().__init__(parent, *args, **kwargs,  bg="#49183A")
        self.account = account
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.widgets()

    def widgets(self):  # pylint: disable=too-many-statements
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
        if self.revealvar.get():
            self.password.config(show="")
        else:
            self.password.config(show="*")

    def login_action(self):
        #messagebox.showinfo("lets goo next logged view","now should open the main budget view ")
        self.master.controller.load_budget_view()
        #if self.master.controller.login(self.username.get(), self.password.get()):
            #messagebox.showinfo("now should open the main budget view ")
            #self.master.controller.load_budget_view()
            # lets goo next logged view

    def register_action(self):
        self.master.controller.load_register_view()
