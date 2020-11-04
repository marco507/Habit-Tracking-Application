
import sqlite3
import login
import analytics
from datetime import date

#Class for creating, deleting and checking habits.
class Habit(object):
       
    def __init__(self):
        #Assign the stored username to the username attribute 
        self.__user = login.User()
        self.__username = self.__user.whoami()
        #Establish the database connection and cursor
        self.__connection = sqlite3.connect('database.db')
        self.__db = self.__connection.cursor() 

    #Checks if a habit exists in a database
    def __check_existence(self, name):
        self.__db.execute('''SELECT * FROM habits WHERE HabitName = ? AND User = ? ''', (name, self.__username))
        exists = self.__db.fetchall()
        return exists

    #Method for creating and storing a habit in the Database
    def create(self, name, period):
        
        #Check if the period value is correct
        if period == "Daily" or period == "Weekly":    

            #Give back an error message if the habit exists
            if self.__check_existence(name):
                print("The habit " + name + " already exists")

            #INSERT the new habit into the database
            else:
                #INSERT Statement
                self.__db.execute('''INSERT INTO habits VALUES(NULL, ?, ?, ?, ?, 0, 0)''', (name, period, self.__username, date.today()))
                #Commit the changes
                self.__connection.commit()
                #Success message
                print("New habit " + name +  " created")

        #Print an error message if the period value is not Daily or Weekly
        else:
            print("Incorrect period")

        #Close the connection
        self.__connection.close()          
        
    #Method for deleting a habit
    def delete(self, name):

        #Check if the habit exists
        if self.__check_existence(name):

            #DELETE Statement
            self.__db.execute('''DELETE FROM habits WHERE HabitName = ? AND User = ?''', (name, self.__username))

            #Commit the changes
            self.__connection.commit()
            #Close the connection
            self.__connection.close() 

        #Give back an error message if the habit does not exists     
        else:    
            print("The habit " + name + " does not exists")
        

    #Hier aufgehört am 04.11 Gehört noch bearbeitet!!!
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

        #Check if the streak is broken



        #Commit the changes
        connection.commit()
        #Close the connection
        connection.close() 


    
#Class for wrapping all functionality for the command line interface
class Pipeline(object):
    
    def __init__(self):
        self.manage = Habit()
        self.analyse = analytics.Analytics()

