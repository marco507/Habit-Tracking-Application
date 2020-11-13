import unittest
import classes
import analytics
import login
import sqlite3
from datetime import date

class TestClasses(unittest.TestCase):

    #Define all necessary settings in setUp
    def setUp(self):
        #Login as test_user
        login.User.login("unittest")
        self.db = sqlite3.connect('database.db').cursor()
    
    #Helper function that queries a habit data entry
    def select_data(self, habitname):
        self.db.execute('''SELECT HabitName FROM habits WHERE HabitName = ?''', (habitname,))
        result = self.db.fetchall()
        return result[0][0]

    #Test for the create method
    def test_create(self):
        #Create a new instance of the class method
        habit = classes.Habit()

        #Enter a predefined habit with the create method
        habit.create("Daily-Habit", "Daily")

        #Search for the inserted habit from the Database and check if the values match
        self.assertEqual("Daily-Habit", self.select_data("Daily-Habit"))

if __name__ == "__main__":
    unittest.main()
