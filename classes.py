
import sqlite3
import login
import analytics
from datetime import date

#Class for creating, deleting and checking habits.
class Habit(object):
    
    #Assign the stored username to the username attribute
    def __init__(self):
        self.user = login.User()
        self.username = self.user.whoami()
        
    #Method for creating and storing a habit in the Database
    def create(self, name, period):
        #Establish DB connection
        connection = sqlite3.connect('database.db')
        # Create a cursor for Database Interaction
        db = connection.cursor()
        
        
        #Check if the habit already exists
        db.execute('''SELECT * FROM habits WHERE HabitName = ? AND User = ? ''', (name, self.username))
        exists = db.fetchall()

        #Give back an error message if the habit exists
        if exists:
           print("The habit " + name + " already exists")

        #INSERT the new habit into the database
        else:
            #INSERT Statement
            db.execute('''INSERT INTO habits VALUES(NULL, ?, ?, ?, ?, 0, 0)''', (name, period, self.username, date.today()))
            #Commit the changes
            connection.commit()

        #Close the connection
        connection.close()          
        
    #Method for deleting a habit
    def delete(self, name):
        #Establish DB connection
        connection = sqlite3.connect('database.db')
        # Create a cursor for Database Interaction
        db = connection.cursor()
        
        #DELETE Statement
        db.execute('''DELETE FROM habits WHERE HabitName = ? AND User = ?''', (name, self.username))
        
        #Commit the changes
        connection.commit()
        #Close the connection
        connection.close() 

    def check(self, name):
        #Establish DB connection
        connection = sqlite3.connect('database.db')
        # Create a cursor for Database Interaction
        db = connection.cursor()

        #Return the HabitID from the database
        db.execute('''SELECT HabitID FROM habits WHERE HabitName = ? AND User = ?''', (name, self.username))
        result = db.fetchall()

        #Extracting the numeric value from the returned list of tuples
        for i in result:
            for j in i:
                habit_id = j
        
        #INSERT a new entry in the tracking data table
        db.execute('''INSERT INTO trackingdata VALUES(NULL, ?, ?)''',  (date.today(), habit_id))


        #Commit the changes
        connection.commit()
        #Close the connection
        connection.close() 


    
#Class for wrapping all functionality for the command line interface
class Pipeline(object):
    
    def __init__(self):
        self.manage = Habit()
        self.analyse = analytics.Analytics()
