
import pandas as pd
import sqlite3
import login

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

#Helper function for checking the existence of a habit
def check_existence(habit):
    
    #Query the habit from the database
    def query_data(db, user):
        return db.execute('''SELECT * FROM habits WHERE HabitName = ? AND User = ? ''', (habit, user))

    #Return the list, an empty list == False, a list with an entry == True
    return retrieve_data(query_data(connect_db(), login.User.whoami())) 

#Helper function for returning an error message
def exit_function():
    print("No data")

#   ------------------CLI Functions------------------
#Class for wrapping all functionality exposed to the user in a single namespace for fire
class Analytics():

    #Testfunktionen    
    @staticmethod
    def show_db():
        #Establish DB connection
        connection = sqlite3.connect('database.db')

        #Query the habits and format it with pandas
        print(pd.read_sql_query("SELECT * FROM habits", connection))

        #Close the connection
        connection.close()          

    @staticmethod
    def show_tracking():
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

        #Query all data from the habits table and return the habits with a list comprehension
        def return_habits(dataset):
            print("User: " + login.User.whoami() + "\nHabits: " + str([i[return_index("HabitName", connect_db())] for i in dataset]))

        #Check if the database is not empty and call the corresponding function
        return_habits(select_data()) if select_data() else exit_function()
        
    #Function for returning all habits with the same period
    @staticmethod
    def similar():
        ''' Function that lists all habits grouped by period '''

        #Query all data from the habits table and return the daily habits with a list comprehension
        def return_daily_habits(dataset):
            print("Daily Habits: " + str([i[return_index("HabitName", connect_db())] for i in dataset if i[return_index("Period", connect_db())] == "Daily"]))
        
        #Query all data from the habits table and return the weekly habits with a list comprehension
        def return_weekly_habits(dataset):   
            print("Weekly Habits: " + str([i[return_index("HabitName", connect_db())] for i in dataset if i[return_index("Period", connect_db())] == "Weekly"]))

        def return_habits():
            return_daily_habits(select_data())
            return_weekly_habits(select_data())  

        #Check if the database is not empty and call the corresponding function
        return_habits() if select_data() else exit_function()

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

            #Define a function for finding the longest streaks corresponding habit
            def return_habit(habits, streaks, longest):
                return habits[streaks.index(longest)]
            
            #Print the result to the terminal
            print("Habit: " + str(return_habit(habit_list(dataset), streak_list(dataset), max(streak_list(dataset)))) +
                "\nStreak: " + str(max(streak_list(dataset))))

        def longest_streak_habit(habit, dataset):
            #Query all data of the logged in user with the select_data function and return the "LongestStreak" value with a list comprehension
            def return_streak(habit, dataset):
                print("Habit: " + habit + 
                    "\nLongest Streak: " + str([i[return_index("LongestStreak", connect_db())] for i in dataset if i[return_index("HabitName", connect_db())] == habit][0]))

            #Check if the habit exists in the database
            exit_function() if not check_existence(habit) else return_streak(habit, dataset) 

        #Call a function according to the given argument and database condition
        exit_function() if not select_data() else (longest_streak_overall(select_data()) if habit == None else longest_streak_habit(habit, select_data()))

    #Return the current streak of a given habit
    @staticmethod
    def current(habit):
        ''' Function that returns the current streak of a given habit '''

        #Query all data of the logged in user with the select_data function and return the "CurrentStreak" value with a list comprehension
        def return_streak(habit, dataset):
            print("Habit: " + habit + 
                "\nStreak: " + str([i[return_index("CurrentStreak", connect_db())] for i in select_data() if i[return_index("HabitName", connect_db())] == habit][0]))

        #Check if the database is not empty and call the corresponding function
        return_streak(habit, select_data()) if check_existence(habit) else exit_function()

    #Function for returning a habits tracking data
    @staticmethod
    def tracking(habit):
        
        #Return the given habits id
        def return_habit_id(habit, dataset):
            return [i[return_index("HabitID", connect_db())] for i in dataset if i[return_index("HabitName", connect_db())] == habit][0]

        #Return all tracking data
        def return_tracking(habit_id):
        
            #Query all tracking data
            def query_tracking_data(db, habit_id):
                return db.execute('''SELECT * FROM trackingdata WHERE HabitID = ?''', (habit_id,))

            #Return the dataset
            return retrieve_data(query_tracking_data(connect_db(), return_habit_id(habit, select_data())))

        #Print the tracking date entries with the help of a for loop
        def pretty_print(dataset):
            print("Habit: " + habit + "\nTracking Data: ")
            for i in dataset:
                print(i[1])

        #Print the tracking data entries to the terminal if the habit exists
        pretty_print(return_tracking(return_habit_id(habit, select_data()))) if check_existence(habit) else exit_function()

    #Function for returning all habits with a streak break and the number of streak breaks
    def breaks(habit):
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

        #Print the tracking data with the help of a for loop
        def pretty_print(dictionary):
            for i in dictionary:
                print("Habit : {} \t Breaks : {}".format(i,dictionary[i]))

        #Print the tracking data entries to the terminal if the habit exists
        pretty_print(return_dictionary(breaks_list(select_data()), habit_list(select_data()))) if select_data() else exit_function()