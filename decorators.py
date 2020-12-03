import io
import sys
import os
import user
import sqlite3


# Decorator for capturing print() output
def capture_print(function):
    def wrapper(*args):
        # Return the username
        current_user = user.return_user()
        # Capture the print() output when testuser is logged in
        if current_user == "testuser":
            # Create a StrinIO object
            capturedOutput = io.StringIO()
            # Redirect stdout to the StringIO objects
            sys.stdout = capturedOutput
            # Call the function
            function(*args)
            # Redirect stdout back to the terminal
            sys.stdout = sys.__stdout__
            return capturedOutput.getvalue()

        # Execute the given function normally
        else:
            # If the command format is incorrect raise and error message
            try:
                # Call the function
                function(*args)
            except TypeError:
                # Redirect stdout back to the terminal
                sys.stdout = sys.__stdout__
                # Return an error message
                print("Incorrect command")
    return wrapper


# Decorator for giving the user a message when no data is found
def user_message(function):
    def wrapper(*args):
        try:
            # If a function returns a empty value give the user a message else return the value of the
            return function(*args) if any(function(*args)) else "No data"
        except TypeError:
            return "Incorrect command"

    return wrapper
