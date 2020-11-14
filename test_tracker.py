import unittest, sqlite3, os, io, sys
import classes, setup, login, analytics
from datetime import date

class TestClasses(unittest.TestCase):

    #Define all necessary settings in setUp
    def setUp(self):
        #First check if a database already exists
        if os.path.exists("database.db"):
            #If the db exists, temporarily rename it
            os.rename("database.db", "database_user.db")

        #Create a new database with the initialize() function
        setup.Database.initialize()

        #Login as test_user
        login.User.login("unittest")

        #Create a new instance of the Habit() class method and establish a database connection
        self.test_habit = classes.Habit()
        self.connection = self.test_habit.connection
        self.db = self.connection.cursor()

    #After completion of the tests restore the correct file structure
    def tearDown(self):
        #Close the db connection
        self.connection.close()

        #Delete the unittest db and rename the user db back to normal if it existed
        os.remove('database.db')
  
        if os.path.exists("database_user.db"):
            os.rename("database_user.db", "database.db")

        #Logout
        login.User.logout()
    
    #Helper function that queries a habit data entry
    def select_data(self, habitname):
        #Query the complete data entry
        self.db.execute('''SELECT * FROM habits WHERE HabitName = ?''', (habitname,))
        result = self.db.fetchall()
        return result

    #Test for the create method
    def test_create(self):
        #Define the testdata
        daily_habit = (1,"Daily-Habit", "Daily", "unittest", str(date.today()), 0, 0, 0)
        weekly_habit = (2,"Weekly-Habit", "Weekly", "unittest", str(date.today()), 0, 0, 0) 

        #First test an entry with a false period value and check the error message
        self.assertEqual("Incorrect period\n", self.test_habit.create("False-Period", "FalseValue"))
        
        #Enter a daily and weekly habit with the create method
        self.test_habit.create("Daily-Habit", "Daily")
        self.test_habit.create("Weekly-Habit", "Weekly")

        #Search for the inserted habit from the Database and check if the values match the defined testdata
        self.assertEqual(daily_habit, self.select_data("Daily-Habit")[0])
        self.assertEqual(weekly_habit, self.select_data("Weekly-Habit")[0])

    #Test for the check method
    #def test_check(self):
        #First check an non existend habit
        #self.assertEqual("The habit NoEntry does not exist\n", self.check("NoEntry"))

        #



          


        #Data entry for checking the daily streak increase

        
        



#Combine all tests
test_suite = unittest.TestSuite()
test_suite.addTest(TestClasses())

    

if __name__ == "__main__":
    #Start the unittest
    unittest.main()


