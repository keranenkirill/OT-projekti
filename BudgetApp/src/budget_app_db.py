import os
import sqlite3

class DataBaseApp:
    def __init__(self, db_path="./budget_app_db.db"):
        self.db_path = db_path
        self.db = None

    def execute_statement(self, query, params):
        try:
            return self.db.execute(query, params)
        except Exception as ex:
            print(ex)
            return False

    def init_database(self):
      try:
            #print("ALUSTETAAN TIETOKANTA...")
            os.remove(self.db_path)
      except Exception as ex:
            print(ex)
         
      try:
            self.db = sqlite3.connect(self.db_path)
            self.db.isolation_level = None
      except Exception as ex:
            print(ex)
            return False
      return True



    def create_tables(self):
        self.db.execute("CREATE TABLE Users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(50) NOT NULL, password TEXT NOT NULL);")
        self.db.execute("CREATE TABLE Expenses (expense_id INTEGER PRIMARY KEY AUTOINCREMENT, amount INTEGER NOT NULL, description TEXT, user_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE);")
        self.db.execute("CREATE TABLE Incomes (income_id INTEGER PRIMARY KEY AUTOINCREMENT, source TEXT NOT NULL, amount INTEGER NOT NULL, user_id INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE);")
   
        

    def create_user(self, uname, psswd):
        self.execute_statement("INSERT INTO Users (username, password) VALUES (?, ?)", [uname, psswd])
        user_id = self.db.execute("SELECT Users.user_id FROM Users WHERE Users.username =?", [uname]).fetchone()
        print("     LISÄTTY ONNISTUNEESTI KAYTTÄJÄ:", uname, " id:", user_id[0])
        return user_id[0]


    def add_expense(self, amnt, descrptn, usr_id):
        self.execute_statement("INSERT INTO Expenses (amount, description, user_id) VALUES (?, ?, ?)", [amnt, descrptn, usr_id])
        print("     LISÄTTY EXPENSE KÄYTTÄJÄLLE ", usr_id, ": MÄÄRÄ:", amnt, " KUVAUS:", descrptn)

    def get_all_expenses(self, user_id):
        kaikki_kulut = self.execute_statement("SELECT Expenses.amount,  Expenses.description FROM Expenses, Users WHERE Users.user_id = Expenses.user_id AND Users.user_id =?;", [user_id]).fetchall()
        print("     HAETTU KÄYTTÄJÄN", user_id, "KAIKKI KULUT:")
        for kulu in kaikki_kulut:
            print("     ", kulu[1], ":", kulu[0])     
        return kaikki_kulut       


    def get_summ_of_all_expenses(self, user_id):
        kulujen_yhteissumma = self.execute_statement("SELECT SUM(Expenses.amount) FROM Expenses, Users WHERE Users.user_id = Expenses.user_id AND Users.user_id =?;", [user_id]).fetchone()
        print("     HAETTU KÄYTTÄJÄN", user_id, "KULUJEN YHTEISSUMMA:")
        print("     ", kulujen_yhteissumma[0])
        return kulujen_yhteissumma[0]


    def add_income(self, src, amnt, usr_id):
            self.execute_statement("INSERT INTO Incomes (source, amount, user_id) VALUES (?, ?, ?)", [src, amnt, usr_id])
            print("     LISÄTTY INCOME KÄYTTÄJÄLLE ", usr_id, ": LÄHDE:", src, " MÄÄRÄ:", amnt)


    def get_all_incomes(self, user_id):
            kaikki_tulot = self.execute_statement("SELECT Incomes.amount,  Incomes.source FROM Incomes, Users WHERE Users.user_id = Incomes.user_id AND Users.user_id =?;", [user_id]).fetchall()
            print("     HAETTU KÄYTTÄJÄN", user_id, "KAIKKI TULOT:")
            for tulo in kaikki_tulot:
                print("     ", tulo[1], ":", tulo[0])


    def get_summ_of_all_incomes(self, user_id):
            tulojen_yhteissumma = self.execute_statement("SELECT SUM(Incomes.amount) FROM Incomes, Users WHERE Users.user_id = Incomes.user_id AND Users.user_id =?;", [user_id]).fetchone()
            print("     HAETTU KÄYTTÄJÄN", user_id, "TULOJEN YHTEISSUMMA:")
            print("     ", tulojen_yhteissumma[0])
            return tulojen_yhteissumma[0]


    def get_income_expense_diff(self, user_id):
            tul_yhtsym = self.get_summ_of_all_incomes(user_id)
            men_yhtsum = self.get_summ_of_all_expenses(user_id)
            print("     HAETTU KÄYTTÄJÄN", user_id, "TULOJEN JA MENOJEN EROTUS:")
            print("     ", tul_yhtsym - men_yhtsum)
            return tul_yhtsym - men_yhtsum
