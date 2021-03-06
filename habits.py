import sqlite3
import io
import sys
import user
import analytics
from decorators import capture_print
from datetime import date, timedelta, datetime

# Class for creating, deleting and checking habits.
class Habit(object):
    def __init__(self):
        # Assign the stored username to the username attribute
        self._username = user.User.whoami()
        # Establish the database connection and cursor
        self._connection = sqlite3.connect("database.db")
        self._db = self._connection.cursor()

    #   ------------------Helper Functions------------------

    # Helper function for checking if a habit exist in a database
    def __check_existence(self, identifier):
        # Check if an ID or name is given as argument
        if type(identifier) is int:
            # Query with the HabitID
            self._db.execute(
                """SELECT * FROM habits WHERE HabitID = ? AND User = ? """,
                (identifier, self._username),
            )
        else:
            # Query with the HabitName
            self._db.execute(
                """SELECT * FROM habits WHERE HabitName = ? AND User = ? """,
                (identifier, self._username),
            )
        exists = self._db.fetchall()
        return exists

    # Helper function for returning the name of a habit with the HabitID
    def __return_name(self, identifier):
        # Check if an ID or name is given as argument
        if type(identifier) is int:
            # Query with the HabitID
            self._db.execute(
                """SELECT HabitName FROM habits WHERE HabitID = ? AND User = ? """,
                (identifier, self._username),
            )
            # Extract the value
            name = self.__extract_value()
            return name
        else:
            # The identifier is already a habit name
            return identifier

    # Helper function for checking if a period exists
    def __check_periods(self, period):
        # Query the periods from the periods table and return the results
        self._db.execute(
            """ SELECT * FROM periods WHERE Period = ? """, (period,))
        exists = self._db.fetchall()
        return exists

    # Helper function for returning the intervall of period
    def __return_intervall(self, period):
        # Query the value from the periods table and return the results
        self._db.execute(
            """ SELECT Intervall FROM periods WHERE Period = ? """, (period,))
        intervall = self.__extract_value()
        return intervall

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
        """ Command for creating a habit """

        # Ensure the correct date for normal program execution
        entry_date = self.__filter_date(entry_date)

        # Check if the name is not only a number
        if type(name) is int:
            print("Wrong name format")

        else:
            # Check if the period value is correct
            if self.__check_periods(period):

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

                    # Return the HabitID from the database
                    self._db.execute(
                        """SELECT HabitID FROM habits WHERE HabitName = ? AND User = ?""",
                        (name, self._username),
                    )
                    # Extracting the numeric value from the returned list of tuples
                    habit_id = self.__extract_value()

                    # Success message
                    print(
                        "New habit "
                        + name
                        + " created"
                        + "\n"
                        + "The habits ID is: "
                        + str(habit_id)
                    )

            # Print an error message if the period is incorrect
            else:
                print("Incorrect period")

    @capture_print
    # Method for deleting a habit
    def delete(self, identifier):
        """ Command for deleting a habit """

        # Check if the habit exists
        if self.__check_existence(identifier):

            # Check if the identifier is a HabitID
            name = self.__return_name(identifier)

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
            print("The habit does not exist")

    @capture_print
    # Method for checking a habit
    def check(self, identifier, entry_date=date.today()):
        """ Command for checking a habit """

        # Ensure the correct date for normal program execution
        entry_date = self.__filter_date(entry_date)

        # Check if the habit exists
        if self.__check_existence(identifier):

            # Check if the identifier is a HabitID
            name = self.__return_name(identifier)

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
                self._db.execute(
                    """SELECT HabitID FROM habits WHERE HabitName = ? AND User = ?""",
                    (name, self._username),
                )
                # Extracting the numeric value from the returned list of tuples
                habit_id = self.__extract_value()

                # Manage the streak
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

                    # Query the period of the given habit
                    self._db.execute(
                        """ SELECT Period FROM habits WHERE HabitID = ? AND User = ? """, (habit_id, self._username))
                    period = self.__extract_value()

                    # Query the intervall of the period
                    self._db.execute(
                        """ SELECT Intervall FROM periods WHERE Period = ? """, (period,))
                    intervall = self.__extract_value()

                    # If the date difference is smaller or euqal the habits intervall, increment the streak
                    if date_difference.days <= intervall:
                        self._db.execute(
                            """UPDATE habits SET CurrentStreak = CurrentStreak + 1 WHERE HabitID = ?""",
                            (habit_id,),
                        )
                        # Print a message if the streak is mantained
                        print("Streak for " + name + " increased")

                    # If the date difference is > intervall set the streak to zero
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
            print("The habit does not exist")

        # Commit the changes
        self._connection.commit()
