
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
        
        #INSERT Statement
        db.execute('''INSERT INTO habits
             VALUES(NULL, ?, ?, ?, ?, 0, 0)''', (name, period, self.username, date.today()))
        
        #Commit the changes
        connection.commit()
        #Close the connection
        connection.close()          
        
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

    
#Class for wrapping all functionality for the command line interface
class Pipeline(object):
    
    def __init__(self):
        self.manage = Habit()
        self.analyse = analytics.Analytics()
