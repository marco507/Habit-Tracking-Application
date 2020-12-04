import sqlite3
import fire
import os
import admin


# Helper function for returning the users table
def return_user():
    # Establish a database connection
    connection = sqlite3.connect("database.db")
    db = connection.cursor()

    # Retrieve the current user
    db.execute(""" SELECT User FROM users """)
    current_user = db.fetchall()
    current_user = current_user[0][0]

    return current_user


# Class for wrapping user-related functions
class User:

    # Store an username in the credentials.txt file
    @staticmethod
    def login(username):
        """ Command for logging-in """

        # Establish a database connection
        connection = sqlite3.connect("database.db")
        db = connection.cursor()

        # Write the given username into the users table
        db.execute(
            """ UPDATE users SET User = ? WHERE UserID = "1" """, (username,))

        connection.commit()

        # Print a succes message only if a real user logs in
        if username != "testuser":
            print("Logged in succesfully")

    # Give back the current user
    @staticmethod
    def whoami():
        """ Command for returning the current user """

        # Query the current user
        user = return_user()

        # Extract the value if it exists and return the username
        if user != "loggedout":
            return user

        # If no user is logged in (loggedout) print an error message
        else:
            print("No user logged in")

    # Delete the username from the credentials.txt file
    @staticmethod
    def logout():
        """ Command for logging-out """

        # Query the current user
        user = return_user()

        # Check if a user is logged in
        if user != "loggedout":
            # Establish a database connection
            # Establish a database connection
            connection = sqlite3.connect("database.db")
            db = connection.cursor()

            # Change the user to "loggedout"
            db.execute(
                """ UPDATE users SET User = "loggedout" WHERE UserID = "1" """)
            connection.commit()

            # Print a message only when a real user is logged in
            if user != "testuser":
                print("Logged out succesfully")
        else:
            print("No user logged in")


if __name__ == "__main__":

    # Initialize the database if it do not exist
    if not os.path.exists("database.db"):
        admin.Database._initialize()

    fire.Fire(User())
