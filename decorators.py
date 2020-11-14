import io, sys
import login

#   ------------------Decorators------------------

#Decorator for capturing print() output
def capture_print(function):

    def wrapper(*args):
        
        #Capture the print() output for the unittest
        if login.User.whoami() == "unittest":
            #Create a StrinIO object
            capturedOutput = io.StringIO() 
            #Redirect stdout to the StringIO objects 
            sys.stdout = capturedOutput
            #Call the function
            function(*args)
            #Redirect stdout back to the terminal
            sys.stdout = sys.__stdout__
            return capturedOutput.getvalue()        

        #Execute the given function normally
        else:
            #If the command format is incorrect raise and error message
            try:
                #Call the function
                function(*args)
            except TypeError:
                #Redirect stdout back to the terminal
                sys.stdout = sys.__stdout__
                #Return an error message
                print("Incorrect command")

    return wrapper

