
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
