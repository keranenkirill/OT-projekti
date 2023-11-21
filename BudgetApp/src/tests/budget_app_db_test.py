import unittest
from budget_app_db import DataBaseApp

class TestDataBaseApp(unittest.TestCase):
   def setUp(self):
      self.budget_app = DataBaseApp()

   def test_init_database(self):
      self.assertNotEqual(self.budget_app.init_database(),True)

