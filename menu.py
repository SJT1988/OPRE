import logging, time, re
from dbM import dbManager as dbM
from helper import helper as h
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

    #================================================================================
    #================================================================================
    # Registration menu
    def register(self):
        #----------------------------------------------------------------------------
        class TooShortError(Exception):
            pass
        #----------------------------------------------------------------------------
        class TooLongError(Exception):
            pass
        #----------------------------------------------------------------------------
        class InvalidCharError(Exception):
            pass
        #----------------------------------------------------------------------------
        class RegexFailError(Exception):
            pass
        #----------------------------------------------------------------------------
        def getUsername() -> str:
            while True:
                print("REGISTRATION - Username")
                print()
                h.printl('Username format:\tUsernames must be between 8 and 20 characters long')
                h.printl('and cannot contain any of the special characters \/:;*?%\"\'<>|')
                icc = 0 #invalid character count

                try:
                    problems = 0            
                    tryUsername = input('Enter new username >>> ')
                    # check the length:
                    if len(tryUsername) < 8:
                        problems+=1
                        raise TooShortError
                    elif len(tryUsername) > 20:
                        problems+=1
                        raise TooLongError
                    # check for invalid characters:
                    for c in tryUsername:
                        if c in '\/:;*?%\"\'<>|':
                            icc+=1
                    if icc > 0:
                        problems+=1
                        raise InvalidCharError
                    # only return if no problems:
                    if problems == 0:
                        return tryUsername

                except TooShortError:
                    logging.info('your username is too short.\n')
                except TooLongError:
                    logging.info('your username is too long.\n')
                except InvalidCharError:
                    logging.info(f'your username contains {icc} invalid characters.')
                finally:
                    time.sleep(1)
                h.clearScreen()
        #----------------------------------------------------------------------------
        def getPassword() -> str:
            while True:
                print("REGISTRATION - Password")
                print()
                h.printl('Password format:\tPasswords must be between 8 and 20 characters long,')
                h.printl('contain both lower and uppercase characters, at least one digt,')
                h.printl('at least one non-word character, and cannot contain any of')
                h.printl('the non-word characters \/:;*?%\"\'<>|')

                try:
                    problems = 0            
                    tryPassword = input('Enter new password >>> ')
                    
                    # check the length:
                    if len(tryPassword) < 8:
                        problems+=1
                        raise TooShortError
                    elif len(tryPassword) > 20:
                        problems+=1
                        raise TooLongError
                    
                    # regex check all character criteria:
                    pattern = '(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*(\W|_))(^[^\/:;*?%\"\'<>|]+$)'
                    match = re.search(pattern, tryPassword)
                    if not match:
                        problems+=1
                        raise RegexFailError
                    
                    # only return if no problems
                    if problems == 0:
                        return tryPassword

                except TooShortError:
                    logging.info('Your password is too short.\n')
                except TooLongError:
                    logging.info('Your password is too long.\n')
                except RegexFailError:
                    logging.info('Your password is not in the required format.')
                finally:
                    time.sleep(1)
                h.clearScreen()
        #----------------------------------------------------------------------------
        def getFname() -> str:
            while True:
                print("REGISTRATION - First Name")
                print()

                try:
                    problems = 0            
                    tryFirstName = input('Enter first name >>> ')
                    fnameLower = tryFirstName.lower()

                    # regex check all character criteria:
                    pattern = '(?=^[a-z ,.\'-]+$)(^[^\/:;*?%\"\'<>|]+$)'
                    match = re.search(pattern, fnameLower)
                    if not match:
                        problems+=1
                        raise RegexFailError
                    
                    # only return if no problems
                    if problems == 0:
                        return tryFirstName

                except RegexFailError:
                    logging.info('Error: avoid the characters \/:;*?%\"\'<>|')
                finally:
                    time.sleep(1)
                h.clearScreen()
        #----------------------------------------------------------------------------
        def getLname() -> str:
            while True:
                print("REGISTRATION - Last Name")
                print()

                try:
                    problems = 0            
                    tryLastName = input('Enter last name >>> ')
                    lnameLower = tryLastName.lower()
                    # regex check all character criteria:
                    pattern = '(?=^[a-z ,.\'-]+$)(^[^\/:;*?%\"\'<>|]+$)'
                    match = re.search(pattern, lnameLower)
                    if not match:
                        problems+=1
                        raise RegexFailError
                    
                    # only return if no problems
                    if problems == 0:
                        return tryLastName

                except RegexFailError:
                    logging.info('Error: avoid the characters \/:;*?%\"\'<>|')
                finally:
                    time.sleep(1)
                h.clearScreen()
        #----------------------------------------------------------------------------
        def getEmail() -> str:
            while True:
                print("REGISTRATION - Email")
                print()

                try:
                    problems = 0            
                    tryEmail = input('Enter email address >>> ')
                    email_lower = tryEmail.lower()
                    # regex check all character criteria:
                    pattern = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
                    match = re.search(pattern, email_lower)
                    if not match:
                        problems+=1
                        raise RegexFailError
                    
                    # only return if no problems
                    if problems == 0:
                        return tryEmail

                except RegexFailError:
                    logging.info('Your email could not be validated.')
                finally:
                    time.sleep(1)
                h.clearScreen()
        #============================================================================

        userName = getUsername()
        password = getPassword()
        firstName = getFname()
        lastName = getLname()
        email = getEmail()
        document = {
            'role': 'customer',
            'username': userName,
            'password': password,
            'nameF': firstName,
            'nameL': lastName,
            'email':email,
            'wallet': 0
        }
        dbM.append_document(document,'Users')

        self.stateName = 'main menu'
        self.state = self.states[self.stateName]
        return

    def specialState(self):
        if self.stateName == 'login':
            logging.info('stateName = login')
            self.login()

        if self.stateName == 'register':
            logging.info('stateName = register')
            self.register()
        if self.stateName == 'quit':
            logging.info('stateName = quit')
            print("Quitting...")
            time.sleep(1)
            exit()
        return
            