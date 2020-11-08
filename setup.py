
import sqlite3
import fire
import os
import login
import classes
from random import seed, randint
from datetime import date, datetime, timedelta

class Database():

    def __init__(self):
        #Establish the database connection and cursor
        self.__connection = sqlite3.connect('database.db')
        self.__db = self.__connection.cursor() 
    
    #Method for the initialisation of the database by creating all default tables
    def initialize(self):
        #Try to create the database tables if the do not already exist
        try:
            # Create a table for storing Habits
            self.__db.execute("""CREATE TABLE habits (
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
            self.__db.execute("""CREATE TABLE trackingdata (
                DataID INTEGER PRIMARY KEY,
                CheckDate DATE NOT NULL,
                HabitID INTEGER NOT NULL,
                FOREIGN KEY (HabitID) REFERENCES habits(HabitID)
            )
            """)

            #Commit the changes
            self.__connection.commit()

            #Print a success message
            print("Database initalized")

        except sqlite3.OperationalError:
            #Print an error message
            print("Database already initialized")

        finally:
            #Close the database connection
            self.__connection.close()
        
    #Method for deleting the database
    def delete(self):
        #Close the database connection
        self.__connection.close()
        #Check if the database file exists and delete it
        if os.path.exists("database.db"):
            os.remove("database.db")
            print("Database deleted")
        #Return an error message if the DB file do not exist
        else:
            print("Database don't exist")

    #Method for inserting the default data
    @staticmethod
    def testdata():
        #Define the default habits
        default_habits = {
            "Workout" : "Daily",
            "Shopping" : "Weekly",
            "Cleaning" : "Weekly",
            "Studying" : "Daily",
            "Reading" : "Daily"
        }
        #Define the creation date of the default habits as 01.10.2020
        default_date = date(2020, 10, 1)

        #Login as test_user
        login.User.login("test_user")
        
        #Insert the default habits with Habit.create() method
        for i in default_habits:
            testdata = classes.Habit()
            testdata.create(i, default_habits[i], default_date)

        #Insert random generated tracking data with the Habit.check() method
        
        #Define the start date and end date for the random entries
        start_date = date(2020, 10, 1)
        end_date= date(2020, 10, 31)

        #Generate a seed for the random habit checks
        seed(1)

        #Set the entry_date to start_date
        entry_date = start_date

        #Loop through all default habits
        
        while entry_date < end_date:
            #Check the habit at the entry_date
            testdata = classes.Habit()
            testdata.check("Workout", entry_date)
            #Generate new random date
            step = randint(1,2)
            entry_date = entry_date + timedelta(days = step)



if __name__ == "__main__":
    #Expose the database class to the command line
    fire.Fire(Database)
