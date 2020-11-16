
import pandas as pd
import sqlite3
import login
from decorators import user_print
from functools import reduce

#   ------------------Helper Functions------------------

#Helper function for establishing a database connection
def connect_db():
    return sqlite3.connect('database.db').cursor()
    
#Helper function for retrieving data from a database cursor
def retrieve_data(db):
    return db.fetchall()

#Helper function for returning the index postion of the habits tables attributes
def return_index(attribute, db):

    #Query the habits table metadata
    def query_metadata(db):
        return db.execute('pragma table_info(habits)')

    #Extract the given attributes index with a list comprehension i[1] is the attribute name
    return [i[1] for i in retrieve_data(query_metadata(db))].index(str(attribute))

#Helper function for querying all user related data and checking if the database is empty
def select_data():
    
    #Query all data for the logged in user
    def query_data(db, user):
        return db.execute('''SELECT * FROM habits WHERE User = ?''', (user,))

    return retrieve_data(query_data(connect_db(), login.User.whoami()))

#   ------------------CLI Functions------------------
#Class for wrapping all functionality exposed to the user in a single namespace for fire
class Analytics():

    #Testfunktion   
    @staticmethod
    def _show_db():
        #Establish DB connection
        connection = sqlite3.connect('database.db')

        #Query the habits and format it with pandas
        print(pd.read_sql_query("SELECT * FROM habits", connection))

        #Close the connection
        connection.close()          

    @staticmethod
    def _show_tracking():
        #Establish DB connection
        connection = sqlite3.connect('database.db')

        #Query the habits and format it with pandas
        print(pd.read_sql_query("SELECT habits.HabitName, habits.User, trackingdata.CheckDate FROM habits INNER JOIN trackingdata ON habits.HabitID = trackingdata.HabitID", connection))

        #Close the connection
        connection.close()  
    
    #Function for returning all habits
    @staticmethod
    def all():
        ''' Function that lists all tracked habits of the logged-in user '''

        return [i[return_index("HabitName", connect_db())] for i in select_data()]
        
    #Function for returning all habits with the same period
    @staticmethod
    def similar(period):
        ''' Function that lists all habits grouped by period '''

        return [i[return_index("HabitName", connect_db())] for i in select_data() if i[return_index("Period", connect_db())] == period]

    #Function for returning the longest streak overall (No argument given) and the longest streak of a habit (Argument = Habit)
    @staticmethod
    def longest(habit = None):
        ''' Function that returns the longest streak overall or of a given habit ''' 
        
        #Search for the longest streak overall
        def longest_streak_overall(dataset):
            #Return the "LongestStreak" values from the dataset with a list comprehension
            def streak_list(dataset):
                return [i[return_index("LongestStreak", connect_db())] for i in dataset]

            #Return the "HabitName" values from the dataset with a list comprehension
            def habit_list(dataset):
                return [i[return_index("HabitName", connect_db())] for i in dataset]

            #Combine the habits and streaks in a dictionary
            def create_dict(habit_list, streak_list):
                return {k: v for k,v in zip(habit_list, streak_list)}

            #Return the habit/s with the longest streak and the longest streak value with a list comprehension
            def max_dict(dictionary):
                return [k for k, v in dictionary.items() if v == max(dictionary.values(), default = [])], max(dictionary.values(), default = [])

            #Return the value
            return max_dict(create_dict(habit_list(select_data()), streak_list(select_data())))
            
        #Search for the longest streak of a given habit
        def longest_streak_habit(habit, dataset):
            #Query all data of the logged in user with the select_data function and return the "LongestStreak" value with a list comprehension
            return [i[return_index("LongestStreak", connect_db())] for i in dataset if i[return_index("HabitName", connect_db())] == habit]
    
        #Call a function according to the given argument with a conditional expression
        return longest_streak_overall(select_data()) if habit == None else longest_streak_habit(habit, select_data())

    #Return the current streak of a given habit
    @staticmethod
    def current(habit):
        ''' Function that returns the current streak of a given habit '''

        #Query all data of the logged in user and return the current streak of a given habit with a list comprehension
        return [i[return_index("CurrentStreak", connect_db())] for i in select_data() if i[return_index("HabitName", connect_db())] == habit]

    #Function for returning a habits tracking data
    @staticmethod
    def tracking(habit):
        
        #Return the given habits id
        def return_habit_id(habit, dataset):
            return max([i[return_index("HabitID", connect_db())] for i in dataset if i[return_index("HabitName", connect_db())] == habit], default = None)

        #Return all tracking data
        def return_tracking(habit_id):
        
            #Query all tracking data entries
            def query_data(db):
                return db.execute('''SELECT CheckDate, HabitID FROM trackingdata''')

            #Filter the data with a list comprehension and return only the habits tracking entries
            def filter_data(dataset, habit_id):
                return [i for i in dataset if habit_id in i]
            
            #Return only the date values
            def return_date(dataset, habit_id):
                return [j for i in dataset for j in i if j != habit_id]

            return return_date(filter_data(retrieve_data(query_data(connect_db())), habit_id), habit_id)
  
        #Return the tracking data entries
        return return_tracking(return_habit_id(habit, select_data()))

    #Function for returning all habits with a streak break and the number of streak breaks
    @staticmethod
    def breaks():
        ''' Function that returns all habits with streak break and the habits number of streak breaks '''

        #Return the "HabitName" values from the dataset with a list comprehension
        def habit_list(dataset):
            return [i[return_index("HabitName", connect_db())] for i in dataset]

        #Return the "Breaks" values from the dataset with a list comprehension
        def breaks_list(dataset):
            return [i[return_index("Breaks", connect_db())] for i in dataset]

        #Return a dictionary with a dictionary comprehension containing all habits with streak breaks
        def return_dictionary(breaks_list, habit_list):
            return {k: v for k,v in zip(habit_list, breaks_list) if v > 0}

        #Return the data
        return return_dictionary(breaks_list(select_data()), habit_list(select_data()))