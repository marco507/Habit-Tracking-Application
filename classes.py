
import sqlite3
import login
import analytics
from datetime import date, timedelta, datetime


#Class for creating, deleting and checking habits.
class Habit(object):
       
    def __init__(self):
        #Assign the stored username to the username attribute 
        self.__username = login.User.whoami()
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
        
    #Method for checking a habit
    def check(self, name):
    
        #Check if the habit exists
        if self.__check_existence(name):

            #Check if an data entry for today already exists
             self.__db.execute('''SELECT * FROM trackingdata WHERE CheckDate = ?''', (date.today(),))
             exists =  self.__db.fetchall()

            #If the habit is already checked return an error message
             if exists:
                 print("The habit is already checked for today")

             else:
                #Return the HabitID from the database
                self.__db.execute('''SELECT HabitID FROM habits WHERE HabitName = ? AND User = ?''', (name, self.__username))
                result = self.__db.fetchall()

                #Extracting the numeric value from the returned list of tuples
                for i in result:
                    for j in i:
                        habit_id = j

                #Check if the streak is interrupted
                #Return the period of the habit from the database
                self.__db.execute('''SELECT Period FROM habits WHERE HabitName = ? AND User = ?''', (name, self.__username))
                result = self.__db.fetchall()

                #Extracting the value for the period from the returned list of tuples
                for i in result:
                    for j in i:
                        period = j

                #Return the last tracking data entry of the habit
                self.__db.execute('''SELECT MAX(CheckDate) FROM trackingdata WHERE HabitID = ?''', (habit_id,))
                result = self.__db.fetchall()

                #Extract the date string from the returned list of tuples
                for i in result:
                    for j in i:
                        last_date = j

                #Convert the string into a datetime object and then into an date object
                last_date = datetime.strptime(last_date, '%Y-%m-%d')
                last_date = last_date.date()

                #Calculate the difference between the last checked date and todays date
                date_difference = date.today() - last_date

                #Check the date difference against the habit period
                #For period the Daily the date difference must be exactly 1 day
                if period == "Daily":
                    #If the date difference is 1 day, increment the streak by 1
                    if date_difference.days == 1:
                        self.__db.execute('''UPDATE habits SET CurrentStreak = CurrentStreak + 1 WHERE HabitID = ?''', (habit_id,))
                    #If the date difference is > 1 set the streak to zero
                    else:
                        self.__db.execute('''UPDATE habits SET CurrentStreak = 0 WHERE HabitID = ?''', (habit_id,))

                #INSERT a new entry in the tracking data table
                self.__db.execute('''INSERT INTO trackingdata VALUES(NULL, ?, ?)''',  (date.today(), habit_id))
                

        #Give back an error message if the habit does not exists     
        else:    
            print("The habit " + name + " does not exists")

        #Commit the changes
        self.__connection.commit()
        #Close the connection
        self.__connection.close() 

    def test(self, name):
        self.__db.execute('''SELECT Period FROM habits WHERE HabitName = ? AND User = ?''', (name, self.__username))
        result = self.__db.fetchall()

        #Extracting the value for the period from the returned list of tuples
        for i in result:
            for j in i:
                period = j

        #Return the HabitID from the database
        self.__db.execute('''SELECT HabitID FROM habits WHERE HabitName = ? AND User = ?''', (name, self.__username))
        result = self.__db.fetchall()

        #Extracting the numeric value from the returned list of tuples
        for i in result:
            for j in i:
                habit_id = j
        
        #Return the last tracking data entry of the habit
        self.__db.execute('''SELECT MAX(CheckDate) FROM trackingdata WHERE HabitID = ?''', (habit_id,))
        result = self.__db.fetchall()

        #Extract the date string from the returned list of tuples
        for i in result:
            for j in i:
                last_date = j

        #Convert the string into a datetime object and then into an date object
        last_date = datetime.strptime(last_date, '%Y-%m-%d')
        last_date = last_date.date()

        #Calculate the difference between the last checked date and todays date
        date_difference = date.today() - last_date

        #Check the date difference against the habit period
        #For period the Daily the date difference must be exactly 1 day
        if period == "Daily":
            #If the date difference is 1 day, increment the streak by 1
            if date_difference.days == 1:
                self.__db.execute('''UPDATE habits SET CurrentStreak = CurrentStreak + 1 WHERE HabitID = ?''', (habit_id,))
            #If the date difference is > 1 set the streak to zero
            else:
                self.__db.execute('''UPDATE habits SET CurrentStreak = 0 WHERE HabitID = ?''', (habit_id,))
        
        self.__connection.commit()

        #Stop am 05.11

        #Close the connection
        self.__connection.close() 


    
#Class for wrapping all functionality for the command line interface
class Pipeline(object):
    
    def __init__(self):
        self.manage = Habit()
        self.analyse = analytics.Analytics()

