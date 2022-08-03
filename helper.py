import os

# module containing helpful functions that could be used
# across all or several modules

class helper():
    
    # Function to clear the screen. Tests for operating system.
    @staticmethod
    def clearScreen():  
        # Windows
        if os.name == 'nt':
            _ = os.system('cls')

        # Mac, Linux(os.name is 'posix')
        else:
            _ = system('clear')
    