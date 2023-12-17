import database  # pylint: disable=import-error
from views.login_view import LoginView  # pylint: disable=import-error
from views.register_view import RegisterView  # pylint: disable=import-error
from views.budget_view import BudgetView  # pylint: disable=import-error


class ViewController():
    """
    Controller class for managing interactions between the application logic and views.

    This class handles the initialization of views, user authentication,
    and interaction with the database through the 'DBController' class.

    Attributes:
    - root: The main application window.
    - context: The currently active view.
    - db: The database controller instance.

    Methods:
    - __init__(self, app): Initializes the ViewController instance.
    - load_register_view(self): Loads the register view, destroying the current context.
    - load_login_view(self, account=""): Loads the login view, destroying the current context.
    - load_budget_view(self): Loads the budget view, destroying the current context.
    - login(self, username, password): Authenticates a user.
    - register(self, username, password): Creates a new user account.
    - get_expenses(self): Retrieves expenses for the current user.
    - get_incomes(self): Retrieves incomes for the current user.
    - get_sum_of_all_expenses(self): Calculates the total sum of all expenses for the current user.
    - get_income_expense_diff(self): Calculates the difference between total incomes and total expenses.
    - add_income(self, *args): Adds a new income for the current user.
    - upd_income(self, *args): Updates an existing income for the current user.
    - add_expense(self, *args): Adds a new expense for the current user.
    - upd_expense(self, *args): Updates an existing expense for the current user.
    - del_expense(self, *args): Deletes an expense for the current user.
    - del_income(self, *args): Deletes an income for the current user.
    """
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

    def get_expenses(self):
        return self.db.get_expenses(self.root.config.user_id)

    def get_incomes(self):
        print("USER", self.root.config.user_id)
        return self.db.get_incomes(self.root.config.user_id)

    def get_sum_of_all_expenses(self):
        return self.db.get_summ_of_all_expenses(self.root.config.user_id)

    def get_income_expense_diff(self):
        return self.db.get_income_expense_diff(self.root.config.user_id)

    def add_income(self, *args):
        print("inputtei", *args)
        return self.db.add_income(*args, usr_id=self.root.config.user_id)

    def upd_income(self, *args):
        return self.db.update_income(*args, usr_id=self.root.config.user_id)

    def add_expense(self, *args):
        return self.db.add_expense(*args, usr_id=self.root.config.user_id)

    def upd_expense(self, *args):
        return self.db.update_expense(*args, usr_id=self.root.config.user_id)

    def del_expense(self, *args):
        return self.db.delete_expense(*args, usr_id=self.root.config.user_id)

    def del_income(self, *args):
        return self.db.delete_income(*args, usr_id=self.root.config.user_id)