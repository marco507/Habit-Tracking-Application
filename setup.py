import sqlite3
import fire
import os
import login
import classes
from random import randint, choice
from datetime import date, datetime, timedelta
from decorators import capture_print

# Class for giving all database related functions a single namespace


class Database:

    # Function for the initialisation of the database by creating all default tables
    @staticmethod
    @capture_print
    def initialize():

        # Create a database and a cursor object
        connection = sqlite3.connect("database.db")
        db = connection.cursor()

        # Try to create the database tables if the do not already exist
        try:
            # Create a table for storing Habits
            db.execute(
                """CREATE TABLE habits (
                HabitID INTEGER PRIMARY KEY,
                HabitName TEXT NOT NULL,
                Period TEXT NOT NULL,
                User TEXT NOT NULL,
                CreationDate DATE NOT NULL,
                CurrentStreak INTEGER NOT NULL,
                LongestStreak INTEGER NOT NULL,
                Breaks INTEGER NOT NULL
            )
            """
            )

            # Create a table for storing tracking data
            db.execute(
                """CREATE TABLE trackingdata (
                DataID INTEGER PRIMARY KEY,
                CheckDate DATE NOT NULL,
                HabitID INTEGER NOT NULL,
                FOREIGN KEY (HabitID) REFERENCES habits(HabitID) ON DELETE CASCADE
            )
            """
            )

            # Commit the changes
            connection.commit()

            # Close the database connection
            connection.close()

            # Return a success message
            print("Database initalized")

        except sqlite3.OperationalError:
            # Return an error message
            print("Database already initialized")

    # Function for deleting the database
    @staticmethod
    def delete():
        # Check if the database file exists and delete it
        if os.path.exists("database.db"):
            os.remove("database.db")
            return "Database deleted"
        # Return an error message if the DB file do not exist
        else:
            print("Database don't exist")

    # Function for inserting the default data
    @staticmethod
    def testdata():

        # Define the default habits
        default_habits = {
            "Workout": "Daily",
            "Shopping": "Weekly",
            "Cleaning": "Weekly",
            "Studying": "Daily",
            "Reading": "Daily",
        }
        # Define the creation date of the default habits as 01.10.2020
        default_date = date(2020, 10, 1)

        # Login as testuser
        login.User.login("testuser")

        # Create a new instane of the Habit() class
        testdata = classes.Habit()

        # Insert the default habits with Habit.create() method
        for i in default_habits:
            testdata.create(i, default_habits[i], default_date)

        # Insert random generated tracking data with the Habit.check() method

        # Define the start date and end date for the random entries
        start_date = date(2020, 10, 1)
        end_date = date(2020, 10, 31)

        # Weigh the possibility for a streak break at 25% for daily habits
        possibility_daily = ["A"] * 75 + ["B"] * 25

        # Weigh the possibility for a streak break at 25% for weekly habits
        # and the chance to check a habit before a week has passed at 15%
        possibility_weekly = ["A"] * 60 + ["B"] * 25 + ["C"] * 15

        # Loop through all default habits
        for i in default_habits:
            # Set the entry_date to start_date
            entry_date = start_date

            # Fill in the tracking data
            while entry_date < end_date:
                # Check the habit at the entry_date
                testdata.check(i, entry_date)

                # Generate new random date
                # Check if the period is daily or weekly
                if default_habits[i] == "Daily":
                    # Choice A = Streak continues = 1 day timediffernence
                    if choice(possibility_daily) == "A":
                        entry_date = entry_date + timedelta(days=1)
                    # Choice B = Streak is broken = random 2 or 3 day timedifference
                    else:
                        entry_date = entry_date + timedelta(days=randint(2, 3))

                else:
                    # Choice A = Streak continues = 7 day timediffernence
                    if choice(possibility_weekly) == "A":
                        entry_date = entry_date + timedelta(days=7)
                    # Choice B = Streak is broken = random 8 to 10 day timedifference
                    elif choice(possibility_weekly) == "B":
                        entry_date = entry_date + \
                            timedelta(days=randint(8, 10))
                    # Choice C = Streak continous = random 4 to 6 day timedifference
                    else:
                        entry_date = entry_date + timedelta(days=randint(4, 6))

            # Set the last tracking entry at the end date (31.10.2020)
            testdata.check(i, end_date)

        # Logout
        login.User.logout()

        # Print a success message
        print("Entered default data")


if __name__ == "__main__":
    # Expose the database class to the command line
    fire.Fire(Database)
