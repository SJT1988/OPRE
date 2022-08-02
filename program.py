import helper, menu, dbManager
import time
from pymongo import MongoClient
import json

m = menu.MenuManager()
dbm = dbManager.dbManager()

def main():
    #m.menu_landing()

    while True:
        print(m.state['message'])

        for i, opt in enumerate(m.state['options']):
            print(f"{i+1}. {opt[0]}")

        answer = input("> ")
        if m.validate(answer, m.state['options']):
            m.state = m.states[m.state['options'][int(answer)-1][1]]
            time.sleep(1.0)
            m.clearScreen()
            break
        else:
            print('\n'.join(["Type the number for one of the given options",
            "and press 'ENTER'."]))

if __name__ == '__main__':
    helper.clearScreen()
    dbm.initialize_minerals_collection()
    main()

