from helper import helper
import logging
import menu
from dbM import dbManager as dbM
import time

m = menu.MenuManager()
LOG_FORMAT = '%(levelname)s :: %(asctime)s -- %(message)s'
logging.basicConfig(
    level=logging.DEBUG, #lowest lvl: every kind of log will be recorded
    format=LOG_FORMAT,
    handlers = [
        logging.FileHandler("OPRE.log"), # log to this file
        logging.StreamHandler() # also log to the console
    ]
)

#================================================================================
#================================================================================
'''
The main program loop is a simple state machine. A state is a dictionary with two
keys: 'message' and 'options' (see 'menu' module). The simplest states are just
menus that are handled in the 'else' block. It reads the 'message' (usually just
the name of a menu) and displays options for more states that the user can access.
if the user's input is validated, the state changes. otherwise, input is requested
until useful input is received.
All complicated states are empty dictionaries (see the 'menu' class for the
reason why) that must be validated differently from conventional menu states.
Checking the length of the current state separates main() into if-else blocks that
prevents validating the state against options the state does not have.
'''
def main():

    while True:
        if len(m.state) == 0: #special state
            m.specialState()
        else: # regular 'ol dict/state
            print(m.state['message'])
            for i, opt in enumerate(m.state['options']):
                print(f'{i+1}. {opt[0]}')

            answer = input('>>> ')
            if m.validate(answer, m.state['options']):
                m.state = m.states[m.state['options'][int(answer)-1][1]]
                time.sleep(1.0)
                helper.clearScreen()
            else:
                print('\n'.join(["Type the number for one of the given options",
                "and press 'ENTER'."]))
                time.sleep(0.5)
        helper.clearScreen()

if __name__ == '__main__':
    '''
    I don't have to run the following b.c. I have already initialized
    the Minerals collection:
    '''
    #dbM.json_to_collection(dbM._users_json_file,'Users')
    #dbM.csv_to_minerals_collection()
    #helper.clearScreen()
    main()

