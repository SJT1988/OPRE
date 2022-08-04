import os

# module containing helpful functions that could be used
# across all or several modules

class helper():

    #================================================================================
    #================================================================================    
    # Function to clear the screen. Tests for operating system.
    @staticmethod
    def clearScreen():  
        # Windows
        if os.name == 'nt':
            _ = os.system('cls')

        # Mac, Linux(os.name is 'posix')
        else:
            _ = system('clear')
    
    #================================================================================
    #================================================================================
    # HELPERS Line formatting wrappers for padding strings.
    # Program width is 80 characters.
    #
    # Left (can't think of a reason to use this one)
    @staticmethod
    def printl(line):
        print(line.ljust(80,' '))
    # Right:
    @staticmethod
    def printr(line):
        print(line.rjust(80,' '))
    # Center:
    @staticmethod
    def printc(line):
        print(line.center(80,' '))

    