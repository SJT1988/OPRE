import csv, json, random, logging
from pymongo import MongoClient
import helper

# Special thanks to RRUFF Project for making their database downloadable
# in csv format
# https://rruff.info/ima/

class dbManager():

    def __init__(self):

        self._minerals_csv_file = 'RRUFF_Export_20220731_223900.csv'
        self._users_json_file = 'users.json'

    #================================================================================
    #================================================================================ 
    # Generates the mineral collection, which is basically an inventory table for our
    # Pet Rock hustle. There are 5,830 real minerals in this collection. I added a
    # Value field that generates a random float (US Dollar amount) from 1 to 1,000.
    # The collection can be construction directly from the list (final method) or
    # from a JSON file if we generate it first (see last pair of commented methods).
    def initialize_minerals_collection(self):
        
        with open(self._minerals_csv_file, 'r', encoding='utf-8') as f:
            # this csv file contains unicode (utf-8) characters that cannot be
            # read (will raise an error) unless we set encoding to utf-8.
            reader = csv.reader(f)
            next(reader) #skips first row, which is just headers
            minerals = []
            for row in reader:
                minerals.append({
                    'MineralID': int(row[2]),
                    'Name': row[0],
                    'Chemistry': row[1],
                    'Country': row[3],
                    'Value': round(1+random.random()*999,2) #guarantees won't be 0
                })
        self.list_to_collection(minerals,'Minerals') # we generated the collection
        # directly from the 'minerals' list but we could also generate, use a json:
        '''
        self.list_to_json(minerals,'minerals.json','utf-8')
        self.json_to_collection('minerals.json','Minerals','utf-8')
        '''
        return

    #================================================================================
    #================================================================================    
    # writes a list of dictionaries to a .json file.
    def list_to_json(self, listOfDicts: list, jsonFile: str, charCode=''):

        # if jsonFile doens't exist, it will be created.
        # if it is not empty, it will be overwritten.
        with open(jsonFile, 'w', encoding=charCode) as f:
            if charCode=='utf-8':
                json.dump(listOfDicts, f, indent = 4, ensure_ascii=False)
                # We need ensure_ascii=False so that utf-8 codes
                # will write as actual characters, not codes.
            else:
                json.dump(listOfDicts, f, indent = 4)
            
        return
    
    #================================================================================
    #================================================================================
    # Creates a MongoDB Collection from a List of dictionaries
    def list_to_collection(self, lstOfDicts: list, collectionName: str):
        client = MongoClient()
        db = client.get_database('project01')
        list_of_collections = db.list_collection_names()
        collection = db[collectionName]
        overwriting = False

        if collectionName in list_of_collections:
            user_in = input(f'collection \'{collectionName}\' already exists. Overwrite? yes = 1, no = 2: ')

            if int(user_in) == 1:
                collection.drop()
                overwriting = True

            elif int(user_in) == 2:
                logging.warning(f'CANCELED: \'{collectionName}\' collection will not be updated.')
                return
            else:
                logging.warning('INVALID INPUT: Canceling.')
                return

        
        collection.insert_many(lstOfDicts)
        if overwriting == True:
            logging.warning(f'SUCCESS: \'{collectionName}\' collection has been overwitten.')       
        else:
            logging.warning(f'SUCCESS: \'{collectionName}\' collection has been created.')
        return
        
    #================================================================================
    #================================================================================
    # Initializes MongoDB collection (from a JSON file)
    def json_to_collection(self, jsonFile: str, collectionName: str, charSet=''):
        client = MongoClient()
        db = client.get_database('project01')
        list_of_collections = db.list_collection_names()
        collection = db[collectionName]
        overwriting = False

        if collectionName in list_of_collections:
            user_in = input(f'collection \'{collectionName}\' already exists. Overwrite? yes = 1, no = 2: ')

            if int(user_in) == 1:
                collection.drop()
                overwriting = True
            elif int(user_in) == 2:
                logging.warning(f'CANCELED: \'{collectionName}\' collection will not be updated.')
                return
            else:
                logging.warning('INVALID INPUT: Canceling.')
                return

        with open(jsonFile, 'r', encoding=charSet) as f:
            file_data = json.load(f)

        collection.insert_many(file_data)
        if overwriting == True:
            logging.warning(f'SUCCESS: \{collectionName}\' collection has been overwitten.')       
        else:
            logging.warning(f'SUCCESS: \'{collectionName}\' collection has been created.')
        return

    #================================================================================
    #================================================================================
    def assign_user_random_pet_rocks(self, userID, count=3):
        client = MongoClient()
        db = client.get_database('project01')
        collection = db.Users
        pass

    #================================================================================
    #================================================================================