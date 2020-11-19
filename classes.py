import sqlite3, io, sys
import login
import analytics
from decorators import capture_print
from datetime import date, timedelta, datetime

# Class for creating, deleting and checking habits.
class Habit(object):
    def __init__(self):
        # Assign the stored username to the username attribute
        self._username = login.User.whoami()
        # Establish the database connection and cursor
        self._connection = sqlite3.connect("database.db")
        self._db = self._connection.cursor()

    #   ------------------Helper Functions------------------

    # Helper function for checking if a habit exist in a database
    def __check_existence(self, name):
        self._db.execute(
            """SELECT * FROM habits WHERE HabitName = ? AND User = ? """,
            (name, self._username),
        )
        exists = self._db.fetchall()
        return exists

    # Helper function for extracting a single value from a returned SELECT query
    def __extract_value(self):
        # Extracting the value from the returned list of tuples
        result = self._db.fetchall()
        result = result[0][0]
        return result

    # Helper function that prevents real users from manipulating date values
    def __filter_date(self, entry_date):
        if self._username != "testuser":
            # Return todays date
            return date.today()
        else:
            # Return the date given as argument back
            return entry_date

    # Method for creating and storing a habit in the Database
    @capture_print
    def create(self, name, period, entry_date=date.today()):

        # Ensure the correct date for normal program execution
        entry_date = self.__filter_date(entry_date)

        # Check if the period value is correct
        if period == "Daily" or period == "Weekly":

            # Give back an error message if the habit exists
            if self.__check_existence(name):
                print("The habit " + name + " already exists")

            # INSERT the new habit into the database
            else:
                # INSERT Statement
                self._db.execute(
                    """INSERT INTO habits VALUES(NULL, ?, ?, ?, ?, 0, 0, 0)""",
                    (name, period, self._username, entry_date),
                )
                # Commit the changes
                self._connection.commit()
                # Success message
                print("New habit " + name + " created")

        # Print an error message if the period value is not Daily or Weekly
        else:
            print("Incorrect period")

    @capture_print
    # Method for deleting a habit
    def delete(self, name):

        # Check if the habit exists
        if self.__check_existence(name):

            # DELETE Statement
            self._db.execute(
                """DELETE FROM habits WHERE HabitName = ? AND User = ?""",
                (name, self._username),
            )

            # Commit the changes
            self._connection.commit()

            # Print a success message
            print("Habit " + name + " deleted")

        # Give back an error message if the habit does not exists
        else:
            print("The habit " + name + " does not exist")

    @capture_print
    # Method for checking a habit
    def check(self, name, entry_date=date.today()):

        # Ensure the correct date for normal program execution
        entry_date = self.__filter_date(entry_date)

        # Check if the habit exists
        if self.__check_existence(name):

            # Check if an data entry for today already exists
            self._db.execute(
                """SELECT * FROM trackingdata INNER JOIN habits ON habits.HabitID = trackingdata.HabitID
                                     WHERE habits.HabitName = ? AND trackingdata.CheckDate = ?""",
                (
                    name,
                    entry_date,
                ),
            )
            exists = self._db.fetchall()

            # If the habit is already checked return an error message
            if exists:
                print("The habit is already checked for today")

            else:
                # Return the HabitID from the database
                self._db.execute(
                    """SELECT HabitID FROM habits WHERE HabitName = ? AND User = ?""",
                    (name, self._username),
                )
                # Extracting the numeric value from the returned list of tuples
                habit_id = self.__extract_value()

                # Manage the streak
                # Return the period of the habit from the database
                self._db.execute(
                    """SELECT Period FROM habits WHERE HabitName = ? AND User = ?""",
                    (name, self._username),
                )
                # Extracting the value for the period from the returned list of tuples
                period = self.__extract_value()

                # Return the last tracking data entry of the habit
                self._db.execute(
                    """SELECT MAX(CheckDate) FROM trackingdata WHERE HabitID = ?""",
                    (habit_id,),
                )
                # Extract the date string from the returned list of tuples
                last_date = self.__extract_value()

                # If the habit is checked the first time increase the streak
                if not last_date:
                    self._db.execute(
                        """UPDATE habits SET CurrentStreak = CurrentStreak + 1 WHERE HabitID = ?""",
                        (habit_id,),
                    )
                    # Print a message if the streak is mantained
                    print("Streak for " + name + " increased")

                # If the habit already has tracking data, check if the streak is interrupted
                else:
                    # Convert the string into a datetime object and then into an date object
                    last_date = datetime.strptime(last_date, "%Y-%m-%d")
                    last_date = last_date.date()

                    # Calculate the difference between the last checked date and the entry date
                    date_difference = entry_date - last_date

                    # Check the date difference against the habit period
                    # For period the Daily the date difference must be exactly 1 day
                    if period == "Daily":
                        # If the date difference is 1 day, increment the streak by 1
                        if date_difference.days == 1:
                            self._db.execute(
                                """UPDATE habits SET CurrentStreak = CurrentStreak + 1 WHERE HabitID = ?""",
                                (habit_id,),
                            )
                            # Print a message if the streak is mantained
                            print("Streak for " + name + " increased")
                        # If the date difference is > 1 set the streak to zero
                        else:
                            # Set the current streak to zero
                            self._db.execute(
                                """UPDATE habits SET CurrentStreak = 0 WHERE HabitID = ?""",
                                (habit_id,),
                            )
                            # Increase the breaks by one
                            self._db.execute(
                                """UPDATE habits SET Breaks = Breaks + 1 WHERE HabitID = ?""",
                                (habit_id,),
                            )
                            # Print a message if the streak is broken
                            print("Streak for " + name + " set to zero")

                    # If the period of the habit is Weekly, the difference must be <= 7
                    else:
                        if date_difference.days <= 7:
                            self._db.execute(
                                """UPDATE habits SET CurrentStreak = CurrentStreak + 1 WHERE HabitID = ?""",
                                (habit_id,),
                            )
                            # Print a message if the streak is mantained
                            print("Streak for " + name + " increased")
                        # If the date difference is > 7 set the streak to zero
                        else:
                            # Set the current streak to zero
                            self._db.execute(
                                """UPDATE habits SET CurrentStreak = 0 WHERE HabitID = ?""",
                                (habit_id,),
                            )
                            # Increase the breaks by one
                            self._db.execute(
                                """UPDATE habits SET Breaks = Breaks + 1 WHERE HabitID = ?""",
                                (habit_id,),
                            )
                            # Print a message if the streak is broken
                            print("Streak for " + name + " set to zero")

                # Check if the current streak is the longest streak

                # Query the current streak
                self._db.execute(
                    """SELECT CurrentStreak FROM habits WHERE HabitID = ?""",
                    (habit_id,),
                )
                # Extract the value from the result
                current_streak = self.__extract_value()

                # Query the longest streak
                self._db.execute(
                    """SELECT LongestStreak FROM habits WHERE HabitID = ?""",
                    (habit_id,),
                )
                # Extract the value from the result
                longest_streak = self.__extract_value()

                # UPDATE the value if the current streak is the longest streak
                if current_streak > longest_streak:
                    self._db.execute(
                        """UPDATE habits SET LongestStreak = ? WHERE HabitID = ?""",
                        (current_streak, habit_id),
                    )

                # INSERT a new entry in the tracking data table
                self._db.execute(
                    """INSERT INTO trackingdata VALUES(NULL, ?, ?)""",
                    (entry_date, habit_id),
                )

        # Give back an error message if the habit does not exists
        else:
            print("The habit " + name + " does not exist")

        # Commit the changes
        self._connection.commit()


# Class for wrapping all functionality for the command line interface
class Pipeline(object):
    def __init__(self):
        self.manage = Habit()
        self.analyse = analytics.Analytics()
