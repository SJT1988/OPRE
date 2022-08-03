import logging, time
from dbM import dbManager as dbM
from helper import helper
# singleton class for handling various I/O functionality
class MenuManager:

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MenuManager, cls).__new__(cls)
        return cls.instance

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
            'login':{},
            'register':{},
            'quit':{},
            'customer menu':{
                'message': 'CUSTOMER MENU',
                'options': [
                    ('Buy Pet Rocks', 'buy'),
                    ('Sell Pet Rocks', 'sell'),
                    ('Transaction History', 'transactions'),
                    ('Account Options', 'customer options'),
                    ('Logoff', 'logoff')
                ]
            },
            'admin menu':{
                'message': 'ADMIN MENU',
                'options': [
                    ('View User Transactions', 'transactions'),
                    ('Delete User', 'delete user'),
                    ('Change User Role', 'change user role'),
                    ('Delete Mineral', 'delete mineral'),
                    ('New Mineral', 'append mineral'),
                    ('Give Pet?', 'append pet'),
                    ('Take Pet!', 'delete pet'),
                    ('Account Options', 'admin options'),
                    ('Logoff', 'logoff')
                ]
            },
            'buy':{},
            'sell':{},
            'customer options':{},
            'admin options':{},
            'delete user':{},
            'change user role':{},
            'delete mineral':{},
            'append mineral':{},
            'delete pet':{},
            'append pet':{},
            'transactions':{},            
            'logoff':{}
        }
        self.state = self.states['main menu']
        self.stateName = 'main menu'

    #================================================================================
    #================================================================================
    # validate input
    def validate(self, ans, opt) -> bool:
        if int(ans) in range(1,len(opt)+1):
            self.stateName = opt[int(ans)-1][1]
            return True
        else:
            return False

    #================================================================================
    #================================================================================
    # HELPER Wrapper for printing faux copywrite info at the top of each screen
    def copyright():
        print('© 2022 ROCK HARD ASSETS, Inc. All Rights Reserved.\n')

    #================================================================================
    #================================================================================
    # HELPER Line formatting wrapper for center print formatting.
    # Program width is 80 characters.
    def printc(line):
        print(line.center(80,' '))

    #================================================================================
    #================================================================================
    # landing menu ((UNUSED)
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

    #================================================================================
    #================================================================================
    # HELPER for Login()
    def change_state_to_role_menu(self):
        role = dbM._user_credentials[2]
        if role == 'admin':
            self.stateName = 'admin menu'
            self.state = self.states[self.stateName]

        elif role == 'customer':
            self.stateName = 'customer menu'
            self.state = self.states[self.stateName]

        else: # raising an exception will close program.
            logging.exception('user\'s role is neither \'customer\' nor \'admin\'.\n')
        return

    def login(self):

        while True:
            inUsername = input('ENTER USERNAME >>> ')
            inPassword = input('ENTER PASSWORD >>> ')

            if dbM.validateLogin(inUsername, inPassword):
                self.change_state_to_role_menu()
                logging.info(f'successful login with credentials {str(dbM._user_credentials)}.')
                break
            else:
                logging.info('failed login')
                print('1. Try Again')
                print('2. Back')
                answer = input('>>> ')
                if int(answer) == 2:
                    self.stateName = 'main menu'
                    self.state = self.states[self.stateName]
                    break
                else: #if user doesn't say '2', just make them go around again.
                    pass
        return

    def specialState(self):
        if self.stateName == 'login':
            logging.info('stateName = login')
            self.login()

        if self.stateName == 'register':
            logging.info('stateName = register')
        if self.stateName == 'quit':
            logging.info('stateName = quit')
            print("Quitting...")
            time.sleep(1)
            exit()
        return
            