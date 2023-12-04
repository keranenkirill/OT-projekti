import database  # pylint: disable=import-error
from views.login_view import LoginView  # pylint: disable=import-error
from views.register_view import RegisterView  # pylint: disable=import-error
from views.budget_view import BudgetView


class ViewController():

    def __init__(self, app):
        self.root = app
        self.context = None
        self.db = database.DBController
        self.db.init_database()
        self.db.create_tables()

    def load_register_view(self):
        if self.context:
            self.context.destroy()
        self.context = RegisterView(self.root)

    def load_login_view(self, account=""):
        if self.context:
            self.context.destroy()
        self.context = LoginView(self.root, account=account)

    def load_budget_view(self):
        if self.context:
            self.context.destroy()
            self.context = BudgetView(self.root)

    def login(self, username, password):
        return self.db.login_user(username, password)

    def register(self, username, password):
        return self.db.create_user(username, password)

