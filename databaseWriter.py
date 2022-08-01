import csv, json, random, logging
from pymongo import MongoClient

# Special thanks to RRUFF Project for making their database downloadable
# in csv format
# https://rruff.info/ima/

_mineral_csv_file = 'RRUFF_Export_20220731_223900.csv'

#================================================================================
#================================================================================ 
# Generates the mineral collection, which is basically an inventory table for our
# Pet Rock hustle. There are 5,830 real minerals in this collection. I added a
# Value field that generates a random float (US Dollar amount) from 1 to 1,000.
def initialize_minerals_collection(mineral_csv_file):
    
    with open(mineral_csv_file, 'r', encoding='utf-8') as f:
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
    
    write_minerals_json(minerals) # Writes list of dicts to JSON file
    # Now we can either write to Collection from the JSON or regen the list:
    # minerals_list_to_collection(minerals) #write to db from list (opt 1)
    minerals_JSON_to_collection('minerals.json') # write to db from JSON (opt 2)
    return

#================================================================================
#================================================================================    
# Generates a JSON file from the downloaded csv file
# I got from the mineral database at RRUFF
def write_minerals_json(minerals_list):

    with open('minerals.json', 'w', encoding='utf-8') as f:
        json.dump(minerals_list, f, indent = 4, ensure_ascii=False)
        # We need ensure_ascii=False so that the utf-8 codes
        # will render as the actual characters, not codes.
    return

#================================================================================
#================================================================================
# Generates MongoDB 'Minerals' collection (ALT1: from a list)
def minerals_list_to_collection(minerals_list):
    client = MongoClient()
    db = client.get_database('project01')
    if not db.Minerals:
        collection = db.Minerals
        collection.insert_many(minerals_list)
    return
    
#================================================================================
#================================================================================
# Generates MongoDB 'Minerals' collection (ALT2: from a JSON file)
def minerals_JSON_to_collection(minerals_json):
    client = MongoClient()
    db = client.get_database('project01')
    list_of_collections = db.list_collection_names()
    overwriting = False

    if 'Minerals' in list_of_collections:
        user_in = input('collection \'Minerals\' already exists. Overwrite? yes = 1, no = 2: ')

        if int(user_in) == 1:
            oldCollection = db.Minerals
            oldCollection.drop()
            overwriting = True
        elif int(user_in) == 2:
            logging.warning('CANCELED: \'Minerals\' collection will not be updated.')
            return
        else:
            logging.warning('INVALID INPUT: Canceling.')
            return

    newCollection = db.Minerals
    with open(minerals_json, 'r', encoding='utf-8') as f:
        file_data = json.load(f)

    newCollection.insert_many(file_data)
    if overwriting == True:
        logging.warning('SUCCESS: \'Minerals\' collection has been overwitten.')       
    else:
        logging.warning('SUCCESS: \'Minerals\' collection has been created.')
    return

#================================================================================
#================================================================================
initialize_minerals_collection('RRUFF_Export_20220731_223900.csv')