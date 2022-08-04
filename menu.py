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
                'message': 'MAIN MENU\n',
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
                'message': 'CUSTOMER MENU\n',
                'options': [
                    ('Buy Pet Rocks', 'buy'),
                    ('Sell Pet Rocks', 'sell'),
                    ('Transaction History', 'transactions'),
                    ('Account Options', 'customer options'),
                    ('Logoff', 'logoff')
                ]
            },
            'admin menu':{
                'message': 'ADMIN MENU\n',
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
        if not re.match('^[0-9]*$', ans):
            return False
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
        time.sleep(1)
        return

    #================================================================================
    #================================================================================
    # Registration menu
    def register(self):
        
        class TooShortError(Exception):
            pass
        #----------------------------------------------------------------------------
        class TooLongError(Exception):
            pass
        #----------------------------------------------------------------------------
        class InvalidCharError(Exception):
            pass
        #----------------------------------------------------------------------------
        class AlreadyExistsError(Exception):
            pass
        #----------------------------------------------------------------------------
        class RegexFailError(Exception):
            pass
        #----------------------------------------------------------------------------
        def getUsername() -> str:
            while True:
                print("REGISTRATION - Username")
                print()
                h.printl('Username format:  Usernames must be between 8 and 20 characters long')
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

                    # check if another user already has this username. Use case-insensitive exact match:
                    if dbM.countMatches({'username': re.compile('^' + tryUsername + '$',re.IGNORECASE)},'Users') > 0:
                        problems+=1
                        raise AlreadyExistsError

                    # only return if no problems:
                    if problems == 0:
                        return tryUsername

                except TooShortError:
                    logging.info('Your username is too short.\n')
                except TooLongError:
                    logging.info('Your username is too long.\n')
                except InvalidCharError:
                    logging.info(f'Your username contains {icc} invalid characters.')
                except AlreadyExistsError:
                    logging.info(f'That username is not available.')
                finally:
                    time.sleep(1)
                h.clearScreen()
        #----------------------------------------------------------------------------
        def getPassword() -> str:
            while True:
                print("REGISTRATION - Password")
                print()
                h.printl('Password format:  Passwords must be between 8 and 20 characters long,')
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
                    
                    # check if another user already has this username. Use case-insensitive exact match:
                    if dbM.countMatches({'email': re.compile('^' + tryEmail + '$',re.IGNORECASE)},'Users') > 0:
                        problems+=1
                        raise AlreadyExistsError

                    # only return if no problems
                    if problems == 0:
                        return tryEmail

                except RegexFailError:
                    logging.info('Your email could not be validated.')
                except AlreadyExistsError:
                    logging.info(f'That email is not available.')
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

    #================================================================================
    #================================================================================
    # logoff 'menu' (airquotes)
    def logoff(self):
        dbM.voidUserCredentials()
        self.stateName = 'main menu'
        self.state = self.states[self.stateName]
        logging.info('Logging off...')
        time.sleep(1)
        h.clearScreen()
        return

    #================================================================================
    #================================================================================
    # Change User Role menu
    def changeUserRole(self):
        
        #----------------------------------------------------------------------------
        def chooseUser() -> str:
           
            while True:
                print('CHANGE USER ROLE')
                print()
                targetUser = input('Enter username of the user whose role will be updated >>> ')
                targetUser = targetUser.strip()
                if not dbM.countMatches({'username': re.compile('^' + targetUser + '$',re.IGNORECASE)},'Users') == 1:
                    logging.error(f'user {targetUser} does not exist. Try again.')
                else:
                    time.sleep(1)
                    h.clearScreen()
                    return targetUser

        #----------------------------------------------------------------------------
        def chooseRole(targetUser) -> str:
            
            while True:
                print('CHANGE USER ROLE')
                print()
                targetRole = input(f'Enter {targetUser}\'s new role >>> ')
                targetRole = targetRole.strip() # helps prevent character mismatch
                targetRole= targetRole.lower() # helps prevent case mismatch
                if targetRole in ['admin', 'customer']:
                    time.sleep(1)
                    h.clearScreen()
                    return targetRole
                else:
                    logging.error('\'Role\' must be either \'customer\' or \'admin\'. Try again.')
                
        #----------------------------------------------------------------------------
        targetUser = chooseUser()
        targetRole = chooseRole(targetUser)
        
        print('CHANGE USER ROLE')
        print()

        result = dbM.updateField({'username': targetUser}, {'role': targetRole}, 'Users')
        if result:
            logging.info(f'Succesfully updated {targetUser}\'s role to \'{targetRole}\'.')
            self.stateName = f'{targetRole} menu'
            self.state = self.states[self.stateName]
        else:
            logging.error(f'Something went wrong updating {targetUser}\'s role.')
            self.stateName = 'main menu'
            self.state = self.states[self.stateName]
        time.sleep(1)
        h.clearScreen()
        return        

    #================================================================================
    #================================================================================
    def deleteUser(self):
        
        userCredentials = dbM.getUserCredentials()
        thisUser = userCredentials[0]
        deleted_self = False

        while True:

            print('DELETE USER')
            print()
            targetUsername = input('Enter the username of the user to delete >>> ')
            logging.error('target is ' + targetUsername)

            # if we try to delete ourself, warn us first
            if targetUsername == thisUser:
                answer = input('Are you sure you want to delete your own account? 1 -> yes, 2 -> no >>> ')
                
                if int(answer) == 1:
                    deleted_self = True

                else: # makes it easy to back-out
                    self.stateName = f'admin menu'
                    self.state = self.states[self.stateName]
                    break # out of loop, to return

            # if no match, try loop again (coninue)
            # regex means (facilitates re.IGNORECASE keyarg, which will give WRONG answer!):
            # if not dbM.countMatches({'username': re.compile('^' + targetUsername + '$'),re.IGNORECASE},'Users')
            logging.error('print count:  ' + str(dbM.countMatches({'username': targetUsername},'Users')))
            if not dbM.countMatches({'username': targetUsername},'Users') == 1:
                logging.error(f'user {targetUsername} does not exist. Try again.')
                continue
            
            document_deleted = dbM.delete_document({'username':targetUsername}, 'Users')
            if document_deleted:
                logging.info(f'successfully deleted {targetUsername}\'s document:\n{document_deleted}.')
                
                if deleted_self:
                    self.stateName = 'main menu'
                    self.state = self.states[self.stateName]
                else:
                    self.stateName = f'admin menu'
                    self.state = self.states[self.stateName]
                break
            else:
                logging.warning(f'failed to delete {targetUsername}\'s document.')
            
            time.sleep(1)
            h.clearScreen()
        
        return
        
        
        
        time.sleep(1)
        return

    #================================================================================
    #================================================================================
    def specialState(self):
        if self.stateName == 'login':
            logging.debug('stateName = login')
            self.login()

        if self.stateName == 'register':
            logging.debug('stateName = register')
            self.register()

        if self.stateName == 'logoff':
            logging.debug('stateName = logoff')
            self.logoff()

        if self.stateName == 'change user role':
            logging.debug('stateName = change user role')
            self.changeUserRole()
        
        if self.stateName == 'delete user':
            logging.debug('stateName = delete user')
            self.deleteUser()

        if self.stateName == 'quit':
            logging.debug('stateName = quit')
            print("Quitting...")
            time.sleep(1)
            exit()
        return
            