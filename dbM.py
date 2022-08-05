from asyncio.windows_events import NULL
import csv, json, random, logging, time
import menu
from pymongo import MongoClient
from helper import helper as h
from pandas import DataFrame
from bson.objectid import ObjectId

# Special thanks to RRUFF Project for making their database downloadable
# in csv format
# https://rruff.info/ima/

client = MongoClient()
db = client.get_database('project01')

class dbManager():

    # class variables:
    _user_credentials = None #(userName,password,role)
    _minerals_csv_file = 'RRUFF_Export_20220731_223900.csv'
    _users_json_file = 'users.json'

    #================================================================================
    #================================================================================
    # Get _user_credentials
    @staticmethod
    def getUserCredentials():
        return dbManager._user_credentials
        
    #================================================================================
    #================================================================================
    # Resets user credentials to None. Used when logging off.
    @staticmethod
    def voidUserCredentials():
        dbManager._user_credentials = None
        return

    #================================================================================
    #================================================================================ 
    # Generates the mineral collection, which is basically an inventory table for our
    # Pet Rock hustle. There are 5,830 real minerals in this collection. I added a
    # Value field that generates a random float (US Dollar amount) from 1 to 1,000.
    # The collection can be construction directly from the list (final method) or
    # from a JSON file if we generate it first (see last pair of commented methods).
    @staticmethod
    def csv_to_minerals_collection():
        
        list_of_collections = db.list_collection_names()
        collectionName = 'Minerals'
        collection = db[collectionName]
        overwriting = False

        if collectionName in list_of_collections:
            user_in = input(f'collection \'{collectionName}\' already exists. Overwrite? yes = 1, no = 2 >>> ')

            if int(user_in) == 1:
                collection.drop()
                overwriting = True

            elif int(user_in) == 2:
                logging.info(f'CANCELED: \'{collectionName}\' collection will not be updated.')
                return
            else:
                logging.warning('INVALID INPUT: Canceling.')
                return

        with open(dbManager._minerals_csv_file, 'r', encoding='utf-8') as f:
            # this csv file contains unicode (utf-8) characters that cannot be
            # read (will raise an error) unless we set encoding to utf-8.
            reader = csv.reader(f)
            next(reader) #skips first row, which is just headers
            for row in reader:
                new_document = {
                    'Name':row[0],
                    'Chemistry':row[1],
                    'Country':row[3],
                    'Value': round(1+random.random()*999,2) #guarantees won't be 0
                }
                db.Minerals.insert_one(new_document)

        if overwriting == True:
            logging.info(f'SUCCESS: \'{collectionName}\' collection has been overwitten.')       
        else:
            logging.info(f'SUCCESS: \'{collectionName}\' collection has been created.')
        return

    #================================================================================
    #================================================================================    
    # writes a list of dictionaries to a .json file.
    @staticmethod
    def list_to_json(listOfDicts: list, jsonFile: str, charCode=''):

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
    @staticmethod
    def list_to_collection(lstOfDicts: list, collectionName: str):

        list_of_collections = db.list_collection_names()
        collection = db[collectionName]
        overwriting = False

        if collectionName in list_of_collections:
            user_in = input(f'collection \'{collectionName}\' already exists. Overwrite? yes = 1, no = 2 >>> ')

            if int(user_in) == 1:
                collection.drop()
                overwriting = True

            elif int(user_in) == 2:
                logging.info(f'CANCELED: \'{collectionName}\' collection will not be updated.')
                return
            else:
                logging.warning('INVALID INPUT: Canceling.')
                return

        
        collection.insert_many(lstOfDicts)
        if overwriting == True:
            logging.info(f'SUCCESS: \'{collectionName}\' collection has been overwitten.')       
        else:
            logging.info(f'SUCCESS: \'{collectionName}\' collection has been created.')
        return
        
    #================================================================================
    #================================================================================
    # Initializes MongoDB collection (from a JSON file)
    @staticmethod
    def json_to_collection(jsonFile: str, collectionName: str, charSet='utf-8'):

        list_of_collections = db.list_collection_names()
        collection = db[collectionName]
        overwriting = False

        if collectionName in list_of_collections:
            user_in = input(f'collection \'{collectionName}\' already exists. Overwrite? yes = 1, no = 2 >>> ')

            if int(user_in) == 1:
                collection.drop()
                overwriting = True
            elif int(user_in) == 2:
                logging.info(f'CANCELED: \'{collectionName}\' collection will not be updated.')
                return
            else:
                logging.info('INVALID INPUT: Canceling.')
                return

        with open(jsonFile, 'r', encoding=charSet) as f:
            file_data = json.load(f)

        collection.insert_many(file_data)
        if overwriting == True:
            logging.info(f'SUCCESS: \'{collectionName}\' collection has been overwitten.')       
        else:
            logging.info(f'SUCCESS: \'{collectionName}\' collection has been created.')
        h.clearScreen()
        return

    #================================================================================
    #================================================================================
    # For a given user (identified by their 'userID' from the User collection),
    # gives them 'quantity' randomly selected pet rocks. Running this outside of the
    # __init__() method will compromise data integrity.
    @staticmethod
    def assign_user_random_pet_rocks(userID, quantity=3):
        uCollection = db.Users
        
        pass

    #================================================================================
    #================================================================================
    #================================================================================
    #================================================================================
    #================================================================================
    #================================================================================
    #================================================================================
    #================================================================================
    # username and password must match the same record for the user's login credentials
    # to be validated.    
    @staticmethod
    def validateLogin(username:str, password:str) -> bool:
        document = db.Users.find_one({'username': username},{'username':1, 'password':1, 'role':1})
        if document != None:
            if document['password'] == password:
                dbManager._user_credentials =(username, password, document['role'])
                logging.info('successful login')
                return True
            else:
                logging.warning('invalid password')
                time.sleep(1)
        else:
            logging.warning('invalid username')
            time.sleep(1)
        return False
    
    #================================================================================
    #================================================================================
    # check if any documents already contain the given key-value pair and return the
    # count. This is just a wrapper for the count_documents() method.
    @staticmethod
    def countMatches(key_value_pair: dict, collectionName: str) -> int:
        return db[collectionName].count_documents(key_value_pair)
    
    #================================================================================
    #================================================================================
    @staticmethod
    def append_document(document: dict, collectionName: str):
        success = True
        try:
            db[collectionName].insert_one(document)
        except:
            logging.error(f'FAILURE: document was not appended to {collectionName}.')
            success = False
        finally:
            time.sleep(1)
            h.clearScreen()
        if success == True:
            logging.info(f'SUCCESS: added document {str(document)} to collection {collectionName}.')
        return

    #================================================================================
    #================================================================================
    # @staticmethod
    # def update_document(collectionName: str, query: dict, update_or_override: dict):
    #     result = db[collectionName].update_one(query, {"$set": update_or_override})
    #     logging.info(result)
    #     return result

    #================================================================================
    #================================================================================
    # wrapper for delete_one()
    @staticmethod
    def delete_document(query: dict, collectionName: str) -> dict:
        
        try:
            result = db[collectionName].delete_one(query)
        except:
            print('INSIDE')
            logging.error(f'FAILED to delete document.')
        finally:
            time.sleep(1)
            h.clearScreen()
        if result:
            logging.info(f'SUCCESSFULLY deleted document.')
        return result
    
    #================================================================================
    #================================================================================
    @staticmethod
    def update_field(match_this: dict, set_this: dict, collectionName: str):

        # result is the updated document or None if the document cannot be found.
        result = db[collectionName].find_one_and_update(match_this, {'$set': set_this})
        logging.debug(result)
        return result

    #================================================================================
    #================================================================================
    @staticmethod
    def tabulateCollection(collectionName: str, first_n_docs = None) -> list:
        
        cursor = db[collectionName].find()
        list_cursor = list(cursor)
        df = DataFrame(list_cursor)
        
        if first_n_docs == None:
            print(df.head())
        else:
            print((df.head(int(first_n_docs))))
        id_list = df['_id'].tolist() # might be useful
        
        return id_list

    #================================================================================
    #================================================================================
    @staticmethod
    def find_and_return_document(collectionName: str, query: dict):
        return db[collectionName].find_one(query)

    #================================================================================
    #================================================================================
    @staticmethod
    def get_id(collectionName:str, query:dict):
        _id = db[collectionName].find_one(query)['_id']
        return _id
    
    #================================================================================
    #================================================================================
    @staticmethod
    def get_myId():
        username = dbManager._user_credentials[0]
        _id = dbManager.get_id('Users',{'username':username})
        return _id
