import fire
import pipeline
import os
import admin
import user

if __name__ == "__main__":

    # Initialize the database if it do not exist
    if not os.path.exists("database.db"):
        admin.Database._initialize()

    # Check if a user is logged in
    if user.return_user() != "loggedout":
        # Expose all functionality to the command line
        fire.Fire(pipeline.Pipeline)

    else:
        print("Log-in first")
