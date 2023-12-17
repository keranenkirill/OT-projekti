import unittest
import sqlite3
from database import DBController as db

class TestDataBaseApp(unittest.TestCase):
    def setUp(self):
        db.db = sqlite3.connect(":memory:")
        db.init_database()
        db.create_tables()
        db.create_user("LasseK", "Nakkipiilo")
        self.cursor = db.db.cursor()

    def tearDown(self):
        db.clear_expenses_by_user_id(1)
        db.clear_incomes_by_user_id(1)

    def test_create_tables(self):
        expected_tables = ["Users", "Expenses", "Incomes"]
        tables = self.cursor.execute(
            'SELECT name FROM sqlite_master WHERE type="table";').fetchall()
        self.assertTrue(all(table in [t[0] for t in tables]
                        for table in expected_tables))

    def test_login_user(self):
        user_id = 1
        username = "LasseK"
        password = "Nakkipiilo"

        logged_in_user_id = db.login_user(username, password)
        self.assertEqual(logged_in_user_id, user_id)

        wrong_password = "WrongPassword"
        logged_in_user_id_wrong_password = db.login_user(
            username, wrong_password)
        self.assertIsNone(logged_in_user_id_wrong_password)

        wrong_username = "WrongUsername"
        logged_in_user_id_wrong_username = db.login_user(
            wrong_username, password)
        self.assertIsNone(logged_in_user_id_wrong_username)

    def test_tables_exist(self):
        expected_tables = ['Users', 'Expenses', 'Incomes']
        self.assertTrue(db.tables_exist())

        existing_tables = db.get_table_names()
        self.assertTrue(
            all(table in existing_tables for table in expected_tables))

    def test_create_user(self):
        nimi = self.cursor.execute(
            'SELECT username FROM Users WHERE Users.username="LasseK";').fetchone()
        self.assertIsNotNone(nimi)

    def test_add_expense(self):
        user_id = 1
        db.add_expense(40, "dna lasku", "Expenses", user_id)
        inserted_datas = self.cursor.execute(
            'SELECT Expenses.amount, Expenses.description, Expenses.user_id FROM Expenses, Users WHERE Users.user_id=Expenses.user_id AND Users.user_id=?;', [user_id]).fetchall()
        inserted_amount, inserted_description, inserted_user_id = inserted_datas[0]
        self.assertEqual(inserted_amount, 40)
        self.assertEqual(inserted_description, "dna lasku")
        self.assertEqual(inserted_user_id, user_id)

    def test_get_all_expenses(self):
        user_id = 1
        txkulut = ["dna", "sijoitus", "vuokra", "netflix", "spotify"]
        for kulu in txkulut:
            db.add_expense(100, kulu, "Expenses", user_id)
        kulut = db.get_expenses(user_id)
        self.assertTrue(all(kulu in [t[1] for t in kulut] for kulu in txkulut))

    def test_get_summ_of_all_expenses(self):
        user_id = 1
        txkulut = ["dna", "sijoitus", "vuokra", "netflix", "spotify"]
        txsumma = len(txkulut)*100
        for kulu in txkulut:
            db.add_expense(100, kulu, "Expenses", user_id)
        self.assertEqual(db.get_summ_of_all_expenses(user_id), txsumma)

    def test_add_income(self):
        user_id = 1
        db.add_income("kela", 340, "Income", user_id)
        inserted_datas = self.cursor.execute(
            'SELECT Incomes.source, Incomes.amount FROM Incomes, Users WHERE Users.user_id = Incomes.user_id AND Users.user_id =?;', [user_id]).fetchall()
        inserted_amount, inserted_source = inserted_datas[0]
        self.assertEqual(inserted_source, "kela")
        self.assertEqual(inserted_amount, "340")

    def test_get_income_expense_diff(self):
        user_id = 1
        db.add_expense(50, "Groceries", "Expenses", user_id)
        db.add_income(1000, "Salary", "Income", user_id)
        expected_diff = 1000 - 50
        actual_diff = db.get_income_expense_diff(user_id)
        self.assertEqual(actual_diff, expected_diff)

    def test_get_summ_of_all_incomes(self):
        user_id = 1
        db.add_income(1000, "Salary", "Income", user_id)
        db.add_income(500, "Bonus", "Income", user_id)
        expected_total_income = 1000 + 500
        actual_total_income = db.get_summ_of_all_incomes(user_id)
        self.assertEqual(actual_total_income, expected_total_income)

    def test_get_all_incomes_expenses(self):
        user_id = 1
        db.add_income(1000, "Salary", "Income", user_id)
        db.add_expense(50, "Groceries", "Expenses", user_id)
        all_incomes_expenses = db.get_all_incomes_expenses(user_id)
        print("all_incomes_expenses:", all_incomes_expenses)
        self.assertIsInstance(all_incomes_expenses, list)
        self.assertTrue(all(isinstance(entry, tuple) and len(
            entry) == 4 for entry in all_incomes_expenses))
        first_entry = all_incomes_expenses[0]
        self.assertEqual(first_entry[0], 1000)
        self.assertEqual(first_entry[1], "Salary")
        self.assertEqual(first_entry[2], 50)
        self.assertEqual(first_entry[3], "Groceries")

    def test_delete_expense(self):
        user_id = 1
        expense_amount = 50
        expense_description = "Groceries"
        db.add_expense(expense_amount, expense_description,
                       "Expenses", user_id)
        expenses = db.get_expenses(user_id)
        added_expense_id = expenses[0][3]
        db.delete_expense(expense_amount, expense_description,
                          "Expenses", added_expense_id, user_id)
        expenses_after_deletion = db.get_expenses(user_id)
        self.assertEqual(len(expenses_after_deletion), 0)

    def test_delete_income(self):
        user_id = 1
        income_amount = 1000
        income_source = "Salary"
        db.add_income(income_amount, income_source, "Income", user_id)
        incomes = db.get_incomes(user_id)
        added_income_id = incomes[0][3]
        db.delete_income(income_amount, income_source,
                         "Income", added_income_id, user_id)
        incomes_after_deletion = db.get_incomes(user_id)
        self.assertEqual(len(incomes_after_deletion), 0)

    def test_update_income(self):
        user_id = 1
        initial_amount = 1000
        initial_source = "Salary"
        db.add_income(initial_amount, initial_source, "Income", user_id)
        incomes = db.get_incomes(user_id)
        added_income_id = incomes[0][3]
        new_amount = 1200
        new_source = "Bonus"
       
    def test_update_income(self):
        user_id = 1
        initial_amount = 1000
        initial_source = "Salary"
        db.add_income(initial_amount, initial_source, "Income", user_id)
        incomes = db.get_incomes(user_id)
        added_income_id = incomes[0][3]
        new_amount = 1200
        new_source = "Bonus"
        db.update_income(new_amount, new_source, "Income",
                        added_income_id, user_id)
        updated_incomes = db.get_incomes(user_id)
        updated_income = updated_incomes[0]
        self.assertEqual(updated_income[0], new_amount)
        self.assertEqual(updated_income[1], new_source)
        self.assertEqual(updated_income[2], "Income")
        self.assertEqual(updated_income[3], added_income_id)


    def test_update_expense(self):
        user_id = 1
        initial_amount = 50
        initial_description = "Groceries"
        db.add_expense(initial_amount, initial_description,
                       "Expenses", user_id)
        expenses = db.get_expenses(user_id)
        added_expense_id = expenses[0][3]
        new_amount = 70
        new_description = "Electronics"
        db.update_expense(new_amount, new_description,
                          "Expenses", added_expense_id, user_id)
        updated_expenses = db.get_expenses(user_id)
        updated_expense = updated_expenses[0]
        self.assertEqual(updated_expense[0], new_amount)
        self.assertEqual(updated_expense[1], new_description)
        self.assertEqual(updated_expense[2], "Expenses")
        self.assertEqual(updated_expense[3], added_expense_id)

    def test_clear_user_and_data_by_id(self):
        user_id = db.create_user("Jekku", "PWD")
        db.add_expense(50, "Groceries", "Expenses", user_id)
        db.add_income(1000, "Salary", "Income", user_id)
        db.clear_user_and_data_by_id(user_id)
        deleted_user = db.login_user("Jekku", "PWD")
        self.assertIsNone(deleted_user)
        cleared_expenses = db.get_expenses(user_id)
        cleared_incomes = db.get_incomes(user_id)
        self.assertEqual(len(cleared_expenses), 0)
        self.assertEqual(len(cleared_incomes), 0)