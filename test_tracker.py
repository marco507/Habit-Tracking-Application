import unittest
import classes
import analytics
import login
import sqlite3
from datetime import date

#Establish a virtual database connection and create tables for testing
connection = sqlite3.connect(':memory:')
db = connection.cursor()

db.execute("""CREATE TABLE habits (
    HabitID INTEGER PRIMARY KEY,
    HabitName TEXT NOT NULL,
    Period TEXT NOT NULL,
    User TEXT NOT NULL,
    CreationDate DATE NOT NULL,
    CurrentStreak INTEGER NOT NULL,
    LongestStreak INTEGER NOT NULL,
    Breaks INTEGER NOT NULL
)
""")

#Create a table for storing tracking data
db.execute("""CREATE TABLE trackingdata (
    DataID INTEGER PRIMARY KEY,
    CheckDate DATE NOT NULL,
    HabitID INTEGER NOT NULL,
    FOREIGN KEY (HabitID) REFERENCES habits(HabitID) ON DELETE CASCADE
)
""")



class TestClasses(unittest.TestCase):

    #Define all necessary settings in setUp
    def setUp(self):
        #Login as test_user
        login.User.login("testuser")
        
        

    #Helper function that queries a habit data entry
    def select_data(self, habitname):
        habit.db.execute('''SELECT HabitName FROM habits WHERE HabitName = ?''', (habitname,))
        result = self.db.fetchall()
        return result[0][0]

    #Test for the create method
    def test_create(self):
        #Create a new instance of the class method
        habit = classes.Habit()

        #Enter a predefined habit with the create method
        habit.create("Daily-Habit", "Daily")

        
        


    

    


        

if __name__ == "__main__":
    unittest.main()
