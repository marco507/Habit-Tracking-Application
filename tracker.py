import fire
import classes
import os

if __name__ == "__main__":

    # Check if the database is initialized
    if os.path.exists("database.db"):
        # Check if a user is logged in
        if os.path.exists("credentials.txt"):
            # Expose to the command line
            fire.Fire(classes.Pipeline)
        else:
            print("Please log-in first")
    else:
        print("Please initialize the database")
