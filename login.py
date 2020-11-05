
import fire
import os

#Class for storing and returning user credentials
class User(object):
    
    #Store an username in the credentials.txt file
    def login(self, username):
        credentials = open("credentials.txt", "w")
        credentials.write(username)
        credentials.close()
        print("Logged in succesfully")
        
    #Give back the current user
    @staticmethod
    def whoami():
        #Check if the credentials.txt exist and return the username
        if os.path.exists("credentials.txt"):
            credentials = open("credentials.txt", "r")
            user = credentials.read()
            credentials.close
            return user
        else:
            print("No user logged in")
        
    #Delete the username from the credentials.txt file
    def logout(self):
        #Check if the database file exists and delete it
        if os.path.exists("credentials.txt"):
            os.remove("credentials.txt")
            print("Logged out succesfully")
        else:
            print("No user logged in")
        
        
if __name__ == "__main__":
    fire.Fire(User)
