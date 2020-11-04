
import pandas as pd
import sqlite3

class Analytics():

    def show(self):
        #Establish DB connection
        connection = sqlite3.connect('database.db')

        #Query the habits and format it with pandas
        print(pd.read_sql_query("SELECT * FROM habits", connection))

        #Close the connection
        connection.close()          

    def tracking(self):
        #Establish DB connection
        connection = sqlite3.connect('database.db')

        #Query the habits and format it with pandas
        print(pd.read_sql_query("SELECT habits.HabitName, habits.User, trackingdata.CheckDate FROM habits INNER JOIN trackingdata ON habits.HabitID = trackingdata.HabitID", connection))

        #Close the connection
        connection.close()  