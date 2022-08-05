from bdb import Breakpoint
import logging, time, re
from bson import ObjectId
from dbM import dbManager as dbM
from helper import helper as h
from datetime import datetime
from pandas import DataFrame
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
                    ('Transaction History', 'transactions'),
                    ('Add Money', 'add money'),
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
                    ('Append Mineral', 'append mineral'),
                    ('Logoff', 'logoff')
                ]
            },
            'buy':{},
            'add money':{},
            'delete user':{},
            'change user role':{},
            'delete mineral':{},
            'append mineral':{},
            'transactions':{},            
            'logoff':{}
        }
        self.state = self.states['main menu']
        self.stateName = 'main menu'

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

        if self.stateName == 'buy':
            logging.debug('stateName = buy')
            self.buy()

        if self.stateName == 'change user role':
            logging.debug('stateName = change user role')
            self.changeUserRole()
        
        if self.stateName == 'delete user':
            logging.debug('stateName = delete user')
            self.deleteUser()

        if self.stateName == 'append mineral':
            logging.debug('stateName = append mineral')
            self.appendMineral()

        if self.stateName == 'delete mineral':
            logging.debug('stateName = delete mineral')
            self.deleteMineral()

        if self.stateName == 'add money':
            logging.debug('stateName = add money')
            self.addMoney()

        if self.stateName == 'transactions':
            logging.debug('stateName = transactions')
            self.transactionHistory()

        if self.stateName == 'quit':
            logging.debug('stateName = quit')
            print("Quitting...")
            time.sleep(1)
            exit()
        return
    
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
    def copyright(self):
        print('© 2022 ROCK HARD ASSETS, Inc. All Rights Reserved.\n')

    #================================================================================
    #================================================================================
    # add money to wallet
    def addMoney(self):
        #----------------------------------------------------------------------------
        def get_dollar_amount()->float:
            value = None
            while True:
                try:
                    value = input('Enter the USD amount to transfer to your wallet from your bank.\nCommas will be ignored (ex: 6, $1.00, 3., 0., 1.2): >>> ')
                    value = value.strip(' $') # strip whitespace, dollar sign
                    value_noCommas = value.replace(',','')
                    # check for invalid characters:
                    # regex check all character criteria:
                    pattern = '^((?:\d)+(?:\.)?(?:\d){0,2})$|^((?:\d)*(?:\.)(?:\d){1,2})$'
                    match = re.search(pattern, value_noCommas)
                    if not match:
                        print('please use the correct format.')
                    fltVal = float(value_noCommas)
                    break
                except:
                    logging.warning('Something went wrong. Try another value.')
            time.sleep(1)
            h.clearScreen()
            return fltVal
        #----------------------------------------------------------------------------
        
        print('ADD MONEY')
        print()
        transfer_amount = get_dollar_amount()
        wallet_balance = dbM.find_and_return_document('Users',{'_id': ObjectId(dbM.get_myId())})['wallet']
        new_amount = wallet_balance+transfer_amount
        dbM.update_field({'_id': ObjectId(dbM.get_myId())},{'wallet': new_amount},'Users')
        print('Your new account balance is $'+ '{:.2f}'.format(new_amount) + '.')
        time.sleep(2)
        h.clearScreen()
        self.change_state_to_role_menu()
        return
    
    #================================================================================
    #================================================================================
    def transactionHistory(self):

        myRole = dbM._user_credentials[2]
        if myRole == 'admin':
            target_username = input('Enter the user whose transaction history you want to see >>> ')
            transactions = dbM.find_and_return_document('Users', {'username': target_username})['transactions']
            df = DataFrame(transactions)
            print(df)
            print()
            input('Press any key to continue')

            self.stateName = 'admin menu'
            self.state = self.states[self.stateName]

        elif myRole == 'customer':

            target_username = dbM._user_credentials[0]
            transactions = dbM.find_and_return_document('Users', {'username': target_username})['transactions']
            df = DataFrame(transactions)
            print(df)
            print()
            input('Press any key to continue')
            self.stateName = 'customer menu'
            self.state = self.states[self.stateName]


        else: # raising an exception will close program.
            logging.exception('user\'s role is neither \'customer\' nor \'admin\'.\n')
        return
    #================================================================================
    #================================================================================
    
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

    #================================================================================
    #================================================================================
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
                        break

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
            h.clearScreen()
            return tryUsername
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
                        break

                except TooShortError:
                    logging.info('Your password is too short.\n')
                except TooLongError:
                    logging.info('Your password is too long.\n')
                except RegexFailError:
                    logging.info('Your password is not in the required format.')
                finally:
                    time.sleep(1)
                h.clearScreen()
            h.clearScreen()
            return tryPassword
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
                        break

                except RegexFailError:
                    logging.info('Error: avoid the characters \/:;*?%\"\'<>|')
                finally:
                    time.sleep(1)
                h.clearScreen()
            h.clearScreen()
            return tryFirstName
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
                        break
                except RegexFailError:
                    logging.info('Error: avoid the characters \/:;*?%\"\'<>|')
                finally:
                    time.sleep(1)
                h.clearScreen()
            h.clearScreen()
            return tryLastName
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
                        break

                except RegexFailError:
                    logging.info('Your email could not be validated.')
                except AlreadyExistsError:
                    logging.info(f'That email is not available.')
                finally:
                    time.sleep(1)
                h.clearScreen()
            h.clearScreen()
            return tryEmail
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
            'wallet': 0,
            'transactions':[]
        }
        dbM.append_document(document,'Users')
        #try-hard way to append record. Works, but wasteful in this situtation
        #dbM.update_field({'username': userName},{'transactions': {}}, 'Users')
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
        print('Logging off...')
        time.sleep(2)
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

        result = dbM.update_field({'username': targetUser}, {'role': targetRole}, 'Users')
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
        #----------------------------------------------------------------------------
        def areYouSure(self) -> int:
            
            while True:
                try:
                    answer = input('Are you sure you want to delete your own account? 1 -> yes, 2 -> no >>> ')
                    if int(answer) == 1 or answer.lower() == 'yes' or answer.lower() == 'y':
                        return 1
                    else:
                        print('Cancelling...')
                        return 2
                except:
                    logging.info('invalid input. try again.')
                    print()
        #----------------------------------------------------------------------------    
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
                answer = areYouSure()
                
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

    #================================================================================
    #================================================================================
    
    def deleteMineral(self):
        print('DELETE MINERAL')
        print()

        id_list = dbM.tabulateCollection('Minerals', 20)
        
        print()
        i = input('Enter the index (not _id) of the Mineral to be deleted\nor press \'ENTER\' to cancel >>> ')
        print()
        if not i == '':
            time.sleep(0.5)
            dbM.delete_document({'_id': id_list[int(i)]},'Minerals')

        self.stateName='admin menu'
        self.state = self.states[self.stateName]
        time.sleep(1)
        return
    #================================================================================
    #================================================================================
    def appendMineral(self):
        #----------------------------------------------------------------------------
        class FormatError(Exception):
            pass
        #----------------------------------------------------------------------------
        def new_name()->str:
            name = None
            while True:
                try:
                    name = input('Enter new mineral\'s name: >>> ')
                    # check for invalid characters:
                    for c in name:
                        if c in '\/:;*?%\"\'<>|':
                            raise FormatError
                    break
                except:
                    logging.warning('Something went wrong. Try another name.')
            time.sleep(1)
            h.clearScreen()
            return name
        #----------------------------------------------------------------------------
        def new_chemistry()->str:
            chemistry = None
            while True:
                try:
                    chemistry = input('Enter new mineral\'s chemistry\n(/\:;*?%\"\'<>| disallowed): >>> ')
                    # check for invalid characters:
                    for c in chemistry:
                        if c in '/\:;*?%\"\'<>|':
                            raise FormatError
                    break
                except:
                    logging.warning('Something went wrong. Try another chemistry formula.')
            time.sleep(1)
            h.clearScreen()
            return chemistry
        #----------------------------------------------------------------------------
        def new_country()->str:
            country = None
            while True:
                try:
                    country = input('Enter new mineral\'s country: >>> ')
                    # check for invalid characters:
                    for c in country:
                        if c in '\/:;*?%\"\'<>|':
                            raise FormatError
                    break
                except:
                    logging.warning('Something went wrong. Try another country.')
            time.sleep(1)
            h.clearScreen()
            return country
        #----------------------------------------------------------------------------
        def new_value()->float:
            value = None
            while True:
                try:
                    value = input('Enter new mineral\'s USD value. Commas will be ignored.\n(ex: 6, $1.00, 3., 0., 1.2): >>> ')
                    value = value.strip(' $') # strip whitespace, dollar sign
                    value_noCommas = value.replace(',','')
                    # check for invalid characters:
                    # regex check all character criteria:
                    pattern = '^((?:\d)+(?:\.)?(?:\d){0,2})$|^((?:\d)*(?:\.)(?:\d){1,2})$'
                    match = re.search(pattern, value_noCommas)
                    if not match:
                        raise FormatError
                    fltVal = float(value_noCommas)
                    break
                except:
                    logging.warning('Something went wrong. Try another value.')
            time.sleep(1)
            h.clearScreen()
            return fltVal
        #----------------------------------------------------------------------------
        print('APPEND MINERAL')
        print()
        name = new_name()
        chemistry = new_chemistry()
        country = new_country()
        value = new_value()
        dbM.append_document({
            'Name': name,
            'Chemistry': chemistry,
            'Country': country,
            'Value': value
        },
        'Minerals')
        self.stateName = 'admin menu'
        self.state = self.states[self.stateName]
        time.sleep(1)
        h.clearScreen()
        return

    #================================================================================
    #================================================================================    
    def buy(self):
        #----------------------------------------------------------------------------
        class OutOfRangeError(Exception):
            pass
        #----------------------------------------------------------------------------
        def getIndex(idxList: list[int]):
            while True:
                try:
                    idx = input('Enter the index (not _id) of the Mineral to make your new [virtual] pet rock\nor press \'ENTER\' to cancel >>> ')
                    if idx == '':
                        return

                    if idx != '' and (int(idx)) not in idxList:
                        raise OutOfRangeError    
                    return idx
                except OutOfRangeError:
                    logging.info('index out of range. Please choose an index in range.')
                except:
                    logging.info('invalid format. Please enter an integer in range.')
                finally:
                    time.sleep(1)
                    h.clearScreen
        #----------------------------------------------------------------------------
        def getPetRockName(mineral_name: str)->str:
            while True:
                try:
                    rock_name = input(f'Give your pet {mineral_name} a name >>> ')               
                    return rock_name
                except:
                    logging.info('invalid input. Please give your rock another name.')
                finally:
                    time.sleep(1)
                    h.clearScreen
        #----------------------------------------------------------------------------
        def getPetRockTalent(rock_name: str)->str:
            while True:
                try:
                    talent = input(f'Give {rock_name} a talent! >>> ')            
                    return talent
                except:
                    logging.info('invalid input. Please give your rock another talent.')
                finally:
                    time.sleep(1)
                    h.clearScreen
        #----------------------------------------------------------------------------
        wallet_balance = dbM.find_and_return_document('Users',{'_id': ObjectId(dbM.get_myId())})['wallet']

        while True:
            print('BUY A [virtual] PET ROCK!')
            print()

            if wallet_balance < 0:
                print('You owe us money. We\'re cutting you off, Bub!')
                print()
                time.sleep(1)
                h.clearScreen()
                self.stateName = 'customer menu'
                self.state = self.states[self.stateName]
                return

            # draw table
            mineralIdxLst = dbM.tabulateCollection('Minerals', 25)
            print()
            # get rock index that we want to buy
            i = getIndex(range(25)) #input('Enter the index (not _id) of the Mineral to make your new [virtual] pet rock\nor press \'ENTER\' to cancel >>> ')
            print()

            if i =='':
                h.clearScreen()
                print('returning to menu...')
                time.sleep(1)
                h.clearScreen
                self.stateName = 'customer menu'
                self.state = self.states[self.stateName]
                h.clearScreen()
                return

            # get mineral name
            mineral_id = mineralIdxLst[int(i)]
            mineral_price = dbM.find_and_return_document('Minerals',{'_id': ObjectId(mineral_id)})['Value']

            # make sure we can afford this:
            if wallet_balance < mineral_price:
                print('You can\'t afford this glorious item!')
                time.sleep(1)
                h.clearScreen()
                continue
            else:
                break
        
        # We exit the loop when a sale is going to succeed
        print()
        # personalize your rock
        mineral_name = dbM.find_and_return_document('Minerals',{'_id': ObjectId(mineral_id)})['Name']
        rock_name = getPetRockName(mineral_name)
        rock_talent = getPetRockTalent(rock_name)
        logging.info(f'Buying {rock_name} the {mineral_name} for $' + '{:.2f}'.format(mineral_price) + '.')
        time.sleep(1)

        # take money
        logging.debug(type(wallet_balance))
        dbM.update_field({'_id': ObjectId(dbM.get_myId())},{'wallet': wallet_balance - mineral_price},'Users')
        wallet_balance = dbM.find_and_return_document('Users',{'_id': ObjectId(dbM.get_myId())})['wallet']
        logging.info(f'Your wallet balance is now {wallet_balance}. Have a rocky day!')

        time.sleep(0.5)
        # username = dbM._user_credentials[0]
        # user_id = dbM.get_id('Users',{'username':username})
        user_id = dbM.get_myId()

        new_transaction = {
            'datetime': datetime.now(),
            'transaction type': 'purchase',
            'pet name': rock_name,
            'pet talent': rock_talent,
            'mineral name': mineral_name,
            'amount': -1*mineral_price
        }

        #dbM._db.Users.update_one({'_id':ObjectId(user_id)},{"$push":{'transactions': new_transaction}})
        dbM.update_document('Users',{'_id':ObjectId(user_id)},{"$push":{'transactions': new_transaction}})

        time.sleep(1)
        self.stateName='customer menu'
        self.state = self.states[self.stateName]
        return