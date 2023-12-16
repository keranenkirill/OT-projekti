import unittest
import sqlite3
from database import DBController as db


class TestDataBaseApp(unittest.TestCase):
    def setUp(self):
        db.db = sqlite3.connect(":memory:")
        db.init_database()
        db.create_tables()
        user_id = db.create_user("LasseK", "Nakkipiilo")
        self.cursor = db.db.cursor()

    def tearDown(self):
        db.clear_expenses_by_user_id(1)

    def test_create_tables(self):
        # assume created in setup
        expected_tables = ["Users", "Expenses", "Incomes"]
        tables = self.cursor.execute(
            'SELECT name FROM sqlite_master WHERE type="table";').fetchall()
        self.assertTrue(all(table in [t[0] for t in tables]
                        for table in expected_tables))

    def test_create_user(self):
        # assume created in setup
        nimi = self.cursor.execute(
            'SELECT username FROM Users WHERE Users.username="LasseK";').fetchone()
        self.assertIsNotNone(nimi)

    def test_add_expense(self):
        user_id = 1
        db.add_expense(40, "dna lasku","Expenses", user_id)
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
            db.add_expense(100, kulu,"Expenses" , user_id)
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
