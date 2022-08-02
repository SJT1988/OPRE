import os

# singleton class for handling various I/O functionality
class MenuManager:

    def __init__(self):
        self.states = {
            'main menu': {
                'message': 'MAIN MENU',
                'options': [
                    ('Login', 'login'),
                    ('Register', 'register'),
                    ('Quit', 'quit')
                ]
            },
            'login':{
                # handle in other module
            },
            'register':{
                # handle in other module
            },
            'quit':{

            }
        }
        self.state = self.states['main menu']

    # validate input
    def validate(self, ans, opt) -> bool:
        if int(ans) in range(1,len(opt)+1):
            #self.state = opt[int(ans)-1][1]
            return True
        else:
            return False

    # Wrapper for printing faux copywrite info at the top of each screen
    def copyright():
        print('© 2022 ROCK HARD ASSETS, Inc. All Rights Reserved.\n')

    # Line formatting wrapper for center print formatting.
    # Program width is 80 characters.
    def printc(line):
        print(line.center(80,' '))

    # landing menu
    def menu_landing(self):
        self.copyright()
        self.printc('WELCOME TO THE PET ROCK')
        self.printc('VIRTUAL EMPORIUM!')
        print('\n')
        self.printc('1.\tLogin')
        self.printc('    2.\tRegister')
        print('\n')
        userIn = input('Please make a selection: >>> ')
        return userIn
    
    # menu
    def menu(self):
        pass