import unittest
from budget_app_db import DataBaseApp

class TestDataBaseApp(unittest.TestCase):
   def setUp(self):
      self.budget_app = DataBaseApp(":memory:")
      self.budget_app.init_database()
      self.budget_app.create_tables()
      user_id = self.budget_app.create_user("LasseK", "")
      self.cursor = self.budget_app.db.cursor()


   def test_create_tables(self):
      # assume created in setup
      expected_tables = ["Users", "Expenses", "Incomes"]
      tables = self.cursor.execute('SELECT name FROM sqlite_master WHERE type="table";').fetchall()
      self.assertTrue(all(table in [t[0] for t in tables] for table in expected_tables))


   def test_create_user(self):
      nimi = self.cursor.execute('SELECT username FROM Users WHERE Users.username="LasseK";').fetchone()
      self.assertIsNotNone(nimi)


   def test_add_expense(self):
      user_id = 1
      self.budget_app.add_expense(40, "dna lasku", user_id)
      inserted_datas = self.cursor.execute('SELECT Expenses.amount, Expenses.description, Expenses.user_id FROM Expenses, Users WHERE Users.user_id=Expenses.user_id AND Users.user_id=?;', [user_id]).fetchall()
      inserted_amount, inserted_description, inserted_user_id = inserted_datas[0]
      self.assertEqual(inserted_amount, 40)
      self.assertEqual(inserted_description, "dna lasku")
      self.assertEqual(inserted_user_id, user_id)
      

   def test_get_all_expenses(self):
      user_id=1
      txkulut = ["dna", "sijoitus", "vuokra", "netflix", "spotify"]
      for kulu in txkulut:
         self.budget_app.add_expense(100, kulu, user_id)
      kulut = self.budget_app.get_all_expenses(user_id)
      self.assertTrue(all(kulu in [t[1] for t in kulut] for kulu in txkulut))


   def test_get_summ_of_all_expenses(self):
      user_id=1
      txkulut = ["dna", "sijoitus", "vuokra", "netflix", "spotify"]
      txsumma= len(txkulut)*100
      for kulu in txkulut:
         self.budget_app.add_expense(100, kulu, user_id)
      self.assertEqual(self.budget_app.get_summ_of_all_expenses(user_id), txsumma)


   def test_add_income(self):
      user_id = 1
      self.budget_app.add_income("kela", 340, user_id)
      inserted_datas = self.cursor.execute('SELECT Incomes.source, Incomes.amount FROM Incomes, Users WHERE Users.user_id = Incomes.user_id AND Users.user_id =?;', [user_id]).fetchall()
      inserted_source, inserted_amount = inserted_datas[0]
      self.assertEqual(inserted_source, "kela")
      self.assertEqual(inserted_amount, 340)



      

