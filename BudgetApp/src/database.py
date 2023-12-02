import os
import sqlite3


class DBController:
    db = None

    @staticmethod
    def execute_statement(query, params):
        try:
            return DBController.db.execute(query, params)
        except Exception as ex:  # pylint: disable=broad-exception-caught
            print(ex)
            return False

    def close():  # pylint: disable=no-method-argument
        DBController.db.close()
        DBController.db = None

    @staticmethod
    def init_database(dbpath="budget_app.db"):
        try:
            DBController.db = sqlite3.connect(
                os.path.join(os.getcwd(), dbpath))
            DBController.db.isolation_level = None
        except Exception as ex:  # pylint: disable=broad-exception-caught
            print(ex)
            return False
        return True

    @staticmethod
    def tables_exist():
        result = DBController.execute_statement(
            "SELECT name FROM sqlite_master WHERE type='table' AND name IN ('Users', 'Expenses', 'Incomes');", [])  # pylint: disable=line-too-long
        return bool(result.fetchone())

    @staticmethod
    def create_tables():
        DBController.db.execute(
            "CREATE TABLE IF NOT EXISTS Users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(50) NOT NULL, password TEXT NOT NULL);")  # pylint: disable=line-too-long
        DBController.db.execute(
            "CREATE TABLE IF NOT EXISTS  Expenses (expense_id INTEGER PRIMARY KEY AUTOINCREMENT, amount INTEGER NOT NULL, description TEXT, user_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE);")  # pylint: disable=line-too-long
        DBController.db.execute(
            "CREATE TABLE IF NOT EXISTS  Incomes (income_id INTEGER PRIMARY KEY AUTOINCREMENT, source TEXT NOT NULL, amount INTEGER NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE);")  # pylint: disable=line-too-long

    @staticmethod
    def create_user(uname, psswd):
        DBController.execute_statement(
            "INSERT INTO Users (username, password) VALUES (?, ?)", [uname, psswd])
        user_id = DBController.db.execute(
            "SELECT Users.user_id FROM Users WHERE Users.username =?", [uname]).fetchone()
        print("     LISÄTTY ONNISTUNEESTI KAYTTÄJÄ:",
              uname, " id:", user_id[0])
        return user_id[0]

    @staticmethod
    def login_user(username, password):
        result = DBController.execute_statement(
            "SELECT username, password FROM Users WHERE username=?", [username]).fetchone()
        print(result)
        if result is not None:
            if result[1] == password:
                return True
        return False

    @staticmethod
    def add_expense(amnt, descrptn, usr_id):
        DBController.execute_statement(
            "INSERT INTO Expenses (amount, description, user_id) VALUES (?, ?, ?)", [amnt, descrptn, usr_id])  # pylint: disable=line-too-long
        print("     LISÄTTY EXPENSE KÄYTTÄJÄLLE ", usr_id,
              ": MÄÄRÄ:", amnt, " KUVAUS:", descrptn)

    @staticmethod
    def get_all_expenses(user_id):
        kaikki_kulut = DBController.execute_statement(
            "SELECT Expenses.amount,  Expenses.description FROM Expenses, Users WHERE Users.user_id = Expenses.user_id AND Users.user_id =?;", [user_id]).fetchall()  # pylint: disable=line-too-long
        print("     HAETTU KÄYTTÄJÄN", user_id, "KAIKKI KULUT:")
        for kulu in kaikki_kulut:
            print("     ", kulu[1], ":", kulu[0])
        return kaikki_kulut

    @staticmethod
    def get_summ_of_all_expenses(user_id):
        kulujen_yhteissumma = DBController.execute_statement(
            "SELECT SUM(Expenses.amount) FROM Expenses, Users WHERE Users.user_id = Expenses.user_id AND Users.user_id =?;", [user_id]).fetchone()  # pylint: disable=line-too-long
        print("     HAETTU KÄYTTÄJÄN", user_id, "KULUJEN YHTEISSUMMA:")
        print("     ", kulujen_yhteissumma[0])
        return kulujen_yhteissumma[0]

    @staticmethod
    def add_income(src, amnt, usr_id):
        DBController.execute_statement(
            "INSERT INTO Incomes (source, amount, user_id) VALUES (?, ?, ?)", [src, amnt, usr_id])  # pylint: disable=line-too-long
        print("     LISÄTTY INCOME KÄYTTÄJÄLLE ",
              usr_id, ": LÄHDE:", src, " MÄÄRÄ:", amnt)

    @staticmethod
    def get_all_incomes(user_id):
        kaikki_tulot = DBController.execute_statement(
            "SELECT Incomes.amount,  Incomes.source FROM Incomes, Users WHERE Users.user_id = Incomes.user_id AND Users.user_id =?;", [user_id]).fetchall()  # pylint: disable=line-too-long
        print("     HAETTU KÄYTTÄJÄN", user_id, "KAIKKI TULOT:")
        for tulo in kaikki_tulot:
            print("     ", tulo[1], ":", tulo[0])
        return kaikki_tulot

    @staticmethod
    def get_summ_of_all_incomes(user_id):
        tulojen_yhteissumma = DBController.execute_statement(
            "SELECT SUM(Incomes.amount) FROM Incomes, Users WHERE Users.user_id = Incomes.user_id AND Users.user_id =?;", [user_id]).fetchone()  # pylint: disable=line-too-long
        print("     HAETTU KÄYTTÄJÄN", user_id, "TULOJEN YHTEISSUMMA:")
        print("     ", tulojen_yhteissumma[0])
        return tulojen_yhteissumma[0]

    @staticmethod
    def get_income_expense_diff(user_id):
        tul_yhtsym = DBController.get_summ_of_all_incomes(user_id)
        men_yhtsum = DBController.get_summ_of_all_expenses(user_id)
        print("     HAETTU KÄYTTÄJÄN", user_id, "TULOJEN JA MENOJEN EROTUS:")
        print("     ", tul_yhtsym - men_yhtsum)
        return tul_yhtsym - men_yhtsum

    @staticmethod
    def clear_expenses_by_user_id(user_id):
        DBController.execute_statement(
            "DELETE FROM Expenses WHERE user_id = ?;", [user_id])
        print(f"Cleared expenses for user with id {user_id}.")

    @staticmethod
    def clear_incomes_by_user_id(user_id):
        DBController.execute_statement(
            "DELETE FROM Incomes WHERE user_id = ?;", [user_id])
        print(f"Cleared incomes for user with id {user_id}.")

    @staticmethod
    def clear_user_and_data_by_id(user_id):
        DBController.execute_statement(
            "DELETE FROM Users WHERE user_id = ?;", [user_id])
        print(f"Deleted user with id {
              user_id} and associated data (expenses and incomes).")
