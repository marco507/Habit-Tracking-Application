
import pandas as pd
import sqlite3
import login

#Class for combining all functions in a single namespace
class Analytics():

    @staticmethod
    def show():
        #Establish DB connection
        connection = sqlite3.connect('database.db')

        #Query the habits and format it with pandas
        print(pd.read_sql_query("SELECT * FROM habits", connection))

        #Close the connection
        connection.close()          

    @staticmethod
    def tracking():
        #Establish DB connection
        connection = sqlite3.connect('database.db')

        #Query the habits and format it with pandas
        print(pd.read_sql_query("SELECT habits.HabitName, habits.User, trackingdata.CheckDate FROM habits INNER JOIN trackingdata ON habits.HabitID = trackingdata.HabitID", connection))

        #Close the connection
        connection.close()  

    #Helper function for querying all user related data
    @staticmethod
    def __select_data():
        #Connect to the database and create a cursor
        connection = connection = sqlite3.connect('database.db')
        db = connection.cursor()
        
        #Query all data related to the actual user without specific conditions
        db.execute('''SELECT * FROM habits WHERE User = ?''', (login.User.whoami(),))
        result = db.fetchall()

        #Close the connection and return the query result
        connection.close()
        return result

    #Helper function for checking the existence of a habit
    @staticmethod
    def __check_existence(name):
        #Connect to the database and create a cursor
        connection = connection = sqlite3.connect('database.db')
        db = connection.cursor()
        
        #Search for the habit in the database
        db.execute('''SELECT * FROM habits WHERE HabitName = ? AND User = ? ''', (name, login.User.whoami()))
        exists = db.fetchall()

        #Close the connection and return the query result
        connection.close()
        return exists


    #Function for printing all habits of the logged in user
    @staticmethod
    def all():
        # 1. Query all data of the logged in user with the __select_data function
        # 2. With a list comprehension create a new list containing only the habits (Habits always have the same index)
        # 3. Print the results to the terminal
        print([i[1] for i in Analytics.__select_data()])
        
    @staticmethod
    def similar():
            # 1. Query all data of the logged in user with the __select_data function
            # 2. With a list comprehension create a new list containing only the daily habits
            # 4. With a list comprehension create a new list containing only the daily habits
            # 5. Print the results to the terminal
            print("Daily Habits: " + str([i[1] for i in Analytics.__select_data() if i[2] == "Daily"]) +
            "\nWeekly Habits: " + str([i[1] for i in Analytics.__select_data() if i[2] == "Weekly"]))

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
                
                def return_streak(habit):
                    # 1. Query all data of the logged in user with the __select_data function
                    # 2. Extract the relevant data with a list comprehension
                    # 3. Print the result to the terminal
                    print("The longest streak for " + habit + " is " + str([i[6] for i in Analytics.__select_data() if i[1] == habit][0]) + " days")

                def exit_function():
                    #Give back an error message if the habit does not exist
                    print("The habit " + habit + " does not exist in the database") 

                #Check if the habit exists in the database
                exit_function() if not Analytics.__check_existence(habit) else return_streak(habit) 

            #Give back an error message if the database is empty
            def exit_function():
                print("The database is empty")

            #Call a function according to the given argument and database condition
            exit_function() if not Analytics.__select_data() else (longest_streak_overall() if habit == None else longest_streak_habit(habit))

    


            
        
        

        