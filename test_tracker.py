import unittest, sqlite3, os, io, sys
import classes, setup, login, analytics
from datetime import date, timedelta

class TestHabit(unittest.TestCase):

    #Define all necessary settings in setUp
    def setUp(self):
        #First check if a database already exists
        if os.path.exists("database.db"):
            #If the db exists, temporarily rename it
            os.rename("database.db", "database_user.db")
        #Create a new database with the initialize() function
        setup.Database.initialize()

        #Create a new instance of the Habit() class method and establish a database connection
        self.test_habit = classes.Habit()
        self.connection = self.test_habit._connection
        self.db = self.connection.cursor()

    #After completion of the tests restore the correct file structure
    def tearDown(self):
        #Close the db connection
        self.connection.close()
        #Delete the unittest db and rename the user db back to normal if it existed
        os.remove('database.db')
        if os.path.exists("database_user.db"):
            os.rename("database_user.db", "database.db")
    
    #Helper function that queries a habit data entry
    def select_data(self, habitname):
        #Query the complete data entry
        self.db.execute('''SELECT * FROM habits WHERE HabitName = ?''', (habitname,))
        result = self.db.fetchall()
        return result

    #Helper function that queries a habit data entry
    def select_tracking(self, habit_id):
        self.db.execute('''SELECT FROM trackingdata WHERE HabitID = ?''', (habit_id))
        result = self.db.fetchall()
        return result

    #Test for the create method
    def test_create(self):
        #Define the testdata to compare against
        daily_habit = (2,"Daily-Habit", "Daily", "testuser", str(date.today()), 0, 0, 0)
        weekly_habit = (3,"Weekly-Habit", "Weekly", "testuser", str(date.today()), 0, 0, 0) 
        
        #Test an entry with a false period value and check the error message
        self.assertEqual("Incorrect period\n", self.test_habit.create("False-Period", "FalseValue"))

        #Test to create a habit that already exists
        #Create a test habit the first time
        self.test_habit.create("DoubleCreate", "Daily")
        #Create the habit the second time and capture the error message
        self.assertEqual("The habit DoubleCreate already exists\n", self.test_habit.create("DoubleCreate", "Daily"))
        
        #Enter a daily and weekly habit with the create method
        self.test_habit.create("Daily-Habit", "Daily")
        self.test_habit.create("Weekly-Habit", "Weekly")

        #Search for the inserted habit from the Database and check if the values match the defined testdata
        self.assertEqual(daily_habit, self.select_data("Daily-Habit")[0])
        self.assertEqual(weekly_habit, self.select_data("Weekly-Habit")[0])

    #Test for the check method
    def test_check(self):
        #Creation Date for the testhabits
        creation_date = str(date(2020, 10, 1))

        #Define the testdata to compare against
        #Data expected from a daily streak increase 
        daily_streak_increase = (2, "IncreaseDaily", "Daily", "testuser", creation_date, 1, 1, 0)
        #Data expected from a weekly streak increase
        weekly_streak_increase = (3, "IncreaseWeekly", "Weekly", "testuser", creation_date, 1, 1, 0)
        #Data expected from a daily streak break
        daily_streak_break = (4, "BreakDaily", "Daily", "testuser", creation_date, 0, 1, 1)
        #Data expected from a weekly streak break
        weekly_streak_break = (5, "BreakWeekly", "Weekly", "testuser", creation_date, 0, 1, 1)

        #Try to check an non existend habit
        self.assertEqual("The habit NoEntry does not exist\n", self.test_habit.check("NoEntry"))

        #Try to check an habit two times on the same day
        #Insert a test entry and check the habit a first time
        self.test_habit.create("DoubleCheck", "Daily")
        self.test_habit.check("DoubleCheck")
        #Catch the error message when trying to check the habit a second time on the same day
        self.assertEqual("The habit is already checked for today\n", self.test_habit.check("DoubleCheck"))

        #Check a daily habit increase of the longest and current streak
        #Insert the test entry
        self.test_habit.create("IncreaseDaily", "Daily", creation_date)
        #Check the habit on the next day
        self.test_habit.check("IncreaseDaily", str(date(2020, 10, 2)))
        #Query the updated data entry in the habits table and compare it to the testdata
        self.assertEqual(daily_streak_increase, self.select_data("IncreaseDaily")[0])

        #Check a weekly habit increase of the longest and current streak
        #Insert the test entry
        self.test_habit.create("IncreaseWeekly", "Weekly", creation_date)
        #Check the habit a week after creation
        self.test_habit.check("IncreaseWeekly", str(date(2020, 10, 7)))
        #Query the updated data entry in the habits table and compare it to the testdata
        self.assertEqual(weekly_streak_increase, self.select_data("IncreaseWeekly")[0])

        #Check a daily habit streak break
        #First insert a new habit
        self.test_habit.create("BreakDaily", "Daily", creation_date)
        #Check the habit a first time to increase the streak
        self.test_habit.check("BreakDaily", date(2020, 10, 2))
        #Check the habit 2 days after to break the streak
        self.test_habit.check("BreakDaily", date(2020, 10, 4))
        #Query the updated data entry in the habits table and compare it to the testdata
        self.assertEqual(daily_streak_break, self.select_data("BreakDaily")[0])

        #Check a weekly habit streak break
        #First insert a new habit
        self.test_habit.create("BreakWeekly", "Weekly", creation_date)
        #Check the habit a first time to increase the streak
        self.test_habit.check("BreakWeekly", date(2020, 10, 2))
        #Check the habit 8 days after to break the streak
        self.test_habit.check("BreakWeekly", date(2020, 10, 10))
        #Query the updated data entry in the habits table and compare it to the testdata
        self.assertEqual(weekly_streak_break, self.select_data("BreakWeekly")[0])

    #Test for the delete() method
    def test_delete(self):
        #Try to delete an non existing habit and capture the error message
        self.assertEqual("The habit NonExisting does not exist\n", self.test_habit.delete("NonExisting"))

        #Insert a test habit
        self.test_habit.create("DeleteMe", "Daily")
        #Delete the habit
        self.test_habit.delete("DeleteMe")
        #Try to query the testhabit
        self.assertFalse(self.select_data("DeleteMe"))

class TestAnalytics(unittest.TestCase):

    #Define all necessary settings in setUp
    def setUp(self):
        #First check if a database already exists
        if os.path.exists("database.db"):
            #If the db exists, temporarily rename it
            os.rename("database.db", "database_user.db")
            #Create a new database with the initialize() function
            setup.Database.initialize()

        #Establish a database connection
        connection = sqlite3.connect("database.db")
        db = connection.cursor()

        #Define the testdata for the habits table
        habit1 = ["Workout", "Daily", "testuser", str(date.today()), 3, 8, 2]
        habit2 = ["Shopping", "Weekly", "testuser", str(date.today()), 1, 3, 5]

        #Define the testdata for the tracking table
        tracking1 = str(date.today())
        tracking2 = str(date.today() + timedelte(days=1))
        tracking2 = str(date.today() + timedelte(days=2))
        
        #Fill the database with test entries
        db.execute('''INSERT INTO habits VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)''', 
        (habit1[0], habit1[1], habit1[2], habit1[3], habit1[4], habit1[5], habit1[6]))

        db.execute('''INSERT INTO habits VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)''', 
        (habit2[0], habit2[1], habit2[2], habit2[3], habit2[4], habit2[5], habit2[6]))

        connection.commit()
        connection.close()

    #After completion of the tests restore the correct file structure
    def tearDown(self):
        #Close the db connection
        self.connection.close()
        #Delete the unittest db and rename the user db back to normal if it existed
        os.remove('database.db')
        if os.path.exists("database_user.db"):
            os.rename("database_user.db", "database.db")



    



#Combine all tests
test_suite = unittest.TestSuite()
test_suite.addTest(TestHabit())
test_suite.addTest(TestAnalytics())

if __name__ == "__main__":
    #Login as testuser
    login.User.login("testuser")
    #Start the unittest
    unittest.main(exit = False)
    #Logout
    login.User.logout()



