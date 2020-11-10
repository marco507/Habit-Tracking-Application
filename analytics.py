
import pandas as pd
import sqlite3
import login

#Class for combining all functions in a single namespace
class Analytics():

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

    #Helper function for querying all user related data and checking if the database is empty
    @staticmethod
    def __select_data():
        
        #Return a connection to the database
        def connect_db():
            return sqlite3.connect('database.db').cursor()

        def query_data(db, user):
            return db.execute('''SELECT * FROM habits WHERE User = ?''', (user,))

        def retrieve_data(db):
            return db.fetchall()

        return retrieve_data(query_data(connect_db(), login.User.whoami()))


    #Helper function for checking the existence of a habit
    @staticmethod
    def __check_existence(name):
        
        #Return a connection to the database
        def connect_db():
            return sqlite3.connect('database.db').cursor()
        
        #Search for the habit in the database
        def query_data(db, user):
            return db.execute('''SELECT * FROM habits WHERE HabitName = ? AND User = ? ''', (name, user))

        def retrieve_data(db):
            return db.fetchall()
 
        return retrieve_data(query_data(connect_db(), login.User.whoami())) 

    #Helper function for returning an error messagepy
    @staticmethod
    def __exit_function():
        print("No data")


    #Function for printing all habits of the logged in user
    @staticmethod
    def all():
        # 1. Query all data of the logged in user with the __select_data function
        # 2. With a list comprehension create a new list containing only the habits (Attributes always have the same index)
        # 3. Print the results to the terminal
        def return_habits(dataset):
            print("User: " + login.User.whoami() + "\nHabits: " + str([i[1] for i in dataset]))

        #Check if the database is not empty and call the corresponding function
        return_habits(Analytics.__select_data()) if Analytics.__select_data() else Analytics.__exit_function()
        
    @staticmethod
    def similar():
        # 1. Query all data of the logged in user with the __select_data function
        # 2. With a list comprehension create a new list containing only the daily habits
        # 4. With a list comprehension create a new list containing only the daily habits
        # 5. Print the results to the terminal
        def return_similar_habits(dataset):
            print("Daily Habits: " + str([i[1] for i in dataset if i[2] == "Daily"]) +
            "\nWeekly Habits: " + str([i[1] for i in dataset if i[2] == "Weekly"]))

        #Check if the database is not empty and call the corresponding function
        return_similar_habits(Analytics.__select_data()) if Analytics.__select_data() else Analytics.__exit_function()

    #Function for returning the longest streak overall (No argument given) and the longest streak of a habit (Argument = Habit)
    @staticmethod
    def longest(habit = None):
        
            #Search for the longest streak overall
            def longest_streak_overall():
                #Define a function for generating a list of all "LongestStreak" values
                def streak_list(dataset):
                    return [i[6] for i in dataset]

                #Define a function for generating a list of all habits
                def habit_list(dataset):
                    return [i[1] for i in dataset]

                #Define a function for finding the longest streak
                def max_streak(streaks):
                    return max(streaks)

                #Define a function for finding the longest streaks corresponding habit
                def return_habit(habits, streaks, longest):
                    return habits[streaks.index(longest)]
                
                #Print the result to the terminal
                print("Habit: " + str(return_habit(habit_list(Analytics.__select_data()), streak_list(Analytics.__select_data()), max_streak(streak_list(Analytics.__select_data())))) +
                "\nStreak: " + str(max_streak(streak_list(Analytics.__select_data()))))

            def longest_streak_habit(habit):
                # 1. Query all data of the logged in user with the __select_data function
                # 2. Extract the relevant data with a list comprehension
                # 3. Print the result to the terminal
                def return_streak(habit):
                    print("Habit: " + habit + "\nLongest Streak: " + str([i[6] for i in Analytics.__select_data() if i[1] == habit][0])) 

                #Check if the habit exists in the database
                Analytics.__exit_function() if not Analytics.__check_existence(habit) else return_streak(habit) 

            #Call a function according to the given argument and database condition
            Analytics.__exit_function() if not Analytics.__select_data() else (longest_streak_overall() if habit == None else longest_streak_habit(habit))

    #Return the current streak of a given habit
    @staticmethod
    def current(habit):
        # 1. Query all data of the logged in user with the __select_data function
        # 2. Extract the relevant data with a list comprehension
        # 3. Print the result to the terminal
        def return_streak(habit, dataset):
            print("Habit: " + habit + "\nStreak: " + str([i[5] for i in Analytics.__select_data() if i[1] == habit][0]))

        #Check if the database is not empty and call the corresponding function
        return_streak(habit, Analytics.__select_data()) if Analytics.__check_existence(habit) else Analytics.__exit_function()

    #Function for returning a habits tracking data
    @staticmethod
    def tracking(habit):
        
        #Return the given habits id
        def return_habit_id(habit, dataset):
            return [i[0] for i in dataset if i[1] == habit][0]

        #Return all tracking data
        def return_tracking(habit_id):
            #Return a connection to the database
            def connect_db():
                return sqlite3.connect('database.db').cursor()

            #Query all tracking data
            def query_data(db, habit_id):
                return db.execute('''SELECT * FROM trackingdata WHERE HabitID = ?''', (habit_id,))

            #Retrieve the data from the cursor
            def retrieve_data(db):
                return db.fetchall()

            #Return the dataset
            return retrieve_data(query_data(connect_db(), return_habit_id(habit, Analytics.__select_data())))

        def pretty_print(dataset):
            print("Habit: " + habit + "\nTracking Data: ")
            for i in dataset:
                print(i[1])

        #Print the tracking data entries to the terminal if the habit exists
        pretty_print(return_tracking(return_habit_id(habit, Analytics.__select_data()))) if Analytics.__check_existence(habit) else Analytics.__exit_function()



