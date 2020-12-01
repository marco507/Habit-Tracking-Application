import fire
import habits
import os

if __name__ == "__main__":

    # Check if the database is initialized
    if os.path.exists("database.db"):
        # Check if a user is logged in
        if os.path.exists("credentials.txt"):
            # Expose to the command line
            fire.Fire(habits.Pipeline)
        else:
            print("Please log-in first")
    else:
        print("Please initialize the database")
