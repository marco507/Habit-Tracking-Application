import sqlite3
import fire
import os
import habits
import user
from random import randint, choice
from datetime import date, datetime, timedelta
from decorators import capture_print

# Class for giving all database related functions a single namespace


class Database:

    # Function for the initialisation of the database by creating all default tables
    @staticmethod
    def _initialize():
        """ Command for creating the database with all default tables """

        # Create a database and a cursor object
        connection = sqlite3.connect("database.db")
        db = connection.cursor()

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

        # Create a table for periods
        db.execute(
            """ CREATE TABLE periods (
                PeriodID INTEGER PRIMARY KEY,
                Period TEXT NOT NULL,
                Intervall INTEGER NOT NULL
            ) 
            """
        )

        # Create a table to store the current user
        db.execute(
            """ CREATE TABLE users (
                UserID INTEGER PRIMARY KEY,
                User TEXT NOT NULL
        )
        """
        )

        # Insert a default user entry
        db.execute(""" INSERT INTO users VALUES (NULL, "loggedout")""")

        # Fill the periods table with the supported periods (Daily, Weekly)
        db.execute(""" INSERT INTO periods Values (NULL, "Daily", "1") """)
        db.execute(""" INSERT INTO periods Values (NULL, "Weekly", "7") """)

        # Commit the changes
        connection.commit()

        # Close the database connection
        connection.close()

    # Function for deleting the database
    @staticmethod
    def reset():
        """ Command for deleting the database """

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
        """ Command for inserting random default data into the database """

        # Check if the database is initialized
        if not os.path.exists("database.db"):
            Database._initialize()

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

        # Save the current username
        current_user = user.User.whoami()

        # Login as testuser
        user.User.login("testuser")

        # Create a new instane of the Habit() class
        testdata = habits.Habit()

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
                        entry_date = entry_date + \
                            timedelta(days=randint(2, 3))

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
                        entry_date = entry_date + \
                            timedelta(days=randint(4, 6))

            # Set the last tracking entry at the end date (31.10.2020)
            testdata.check(i, end_date)

        # Print a success message
        print("Entered default data")


if __name__ == "__main__":
    fire.Fire(Database())
