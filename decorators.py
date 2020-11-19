import io
import sys
import os
import login

# Decorator for capturing print() output


def capture_print(function):
    def wrapper(*args):
        # Check if the credentials.txt exist and return the username
        if os.path.exists("credentials.txt"):
            credentials = open("credentials.txt", "r")
            user = credentials.read()
            credentials.close()
            # Capture the print() output when testuser is logged in
            if user == "testuser":
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

        # Execute all functions normally that require no logged in user (Database)
        else:
            # Call the function
            function(*args)

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
