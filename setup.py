
import sqlite3
import fire
import os

class Database(object):
    
    #Method for the initialisation of the database by creating all default tables
    def initialize(self):
        # Create a new Database
        connection = sqlite3.connect('database.db')

        # Create a cursor for Database Interaction
        db = connection.cursor()

        #Try to create the database tables if the do not already exist
        try:
            # Create a table for storing Habits - FEHLT CreationDate LongestStreak, CurrentStreak, Break
            db.execute("""CREATE TABLE habits (
                HabitID INTEGER PRIMARY KEY,
                HabitName TEXT NOT NULL,
                Period TEXT NOT NULL,
                User TEXT NOT NULL,
                CreationDate DATE NOT NULL,
                CurrentStreak INTEGER NOT NULL,
                LongestStreak INTEGER NOT NULL
            )
            """)

            #Commit the changes
            connection.commit()

            #Print a success message
            print("Database initalized")

        except sqlite3.OperationalError:
            #Print an error message
            print("Database already initialized")

        finally:
            #Close the database connection
            connection.close()
        
    #Method for deleting the database
    def delete(self):
        #Check if the database file exists and delete it
        if os.path.exists("database.db"):
            os.remove("database.db")
            print("Database deleted")
        #Return an error message if the DB file do not exist
        else:
            print("Database don't exist")

if __name__ == "__main__":
    #Expose the database class to the command line
    fire.Fire(Database)
