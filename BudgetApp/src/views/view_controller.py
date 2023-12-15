import database  # pylint: disable=import-error
from views.login_view import LoginView  # pylint: disable=import-error
from views.register_view import RegisterView  # pylint: disable=import-error
from views.budget_view import BudgetView  # pylint: disable=import-error


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

    def get_expenses(self):
        return self.db.get_expenses(self.root.config.id)

    def get_incomes(self):
        print("USER", self.root.config.id)
        return self.db.get_incomes(self.root.config.id)

    def get_sum_of_all_expenses(self):
        return self.db.get_summ_of_all_expenses(self.root.config.id)

    def get_income_expense_diff(self):
        return self.db.get_income_expense_diff(self.root.config.id)

    def add_income(self, *args):
        print("inputtei", *args)
        return self.db.add_income(*args, usr_id=self.root.config.id)

    def upd_income(self, *args):
        return self.db.update_income(*args, usr_id=self.root.config.id)

    def add_expense(self, *args):
        return self.db.add_expense(*args, usr_id=self.root.config.id)

    def upd_expense(self, *args):
        return self.db.update_expense(*args, usr_id=self.root.config.id)

    def del_expense(self, *args):
        return self.db.delete_expense(*args, usr_id=self.root.config.id)

    def del_income(self, *args):
        return self.db.delete_income(*args, usr_id=self.root.config.id)

    def log_out(self):
        pass
