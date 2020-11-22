import fire
import os

# Class for wrapping user-related functions


class User:

    # Store an username in the credentials.txt file
    @staticmethod
    def login(username):
        """ Command for logging-in """

        credentials = open("credentials.txt", "w")
        credentials.write(username)
        credentials.close()
        # Print a succes message only if a real user logs in
        if username != "testuser":
            print("Logged in succesfully")

    # Give back the current user
    @staticmethod
    def whoami():
        """ Command for returning the current user """

        # Check if the credentials.txt exist and return the username
        if os.path.exists("credentials.txt"):
            credentials = open("credentials.txt", "r")
            user = credentials.read()
            credentials.close()
            return user
        else:
            print("No user logged in")

    # Delete the username from the credentials.txt file
    @staticmethod
    def logout():
        """ Command for logging-out """

        # Check if the database file exists and delete it
        if os.path.exists("credentials.txt"):
            # Capture the last username
            username = User.whoami()
            # Delete the credentials file
            os.remove("credentials.txt")
            # Print a message only when a real user is logged in
            if username != "testuser":
                print("Logged out succesfully")
        else:
            print("No user logged in")


if __name__ == "__main__":
    fire.Fire(User)
