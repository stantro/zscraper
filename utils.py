import configparser
from pymongo import MongoClient
import os

def get_config(test=False):

    root = os.path.dirname(__file__)
    config = configparser.ConfigParser()
    config.read_file(open(root+'/config.ini'))

    return config['DEFAULT'] if not test else config['TEST']
    
def get_url(config):

    subdomain, start = config['subdomain'], config['start']

    return f"https://{subdomain}.zendesk.com/api/v2/incremental/tickets?start_time={start}"

def init_db(config):
    
    host, database , collection = config['host'], config['database'], config['collection']

    database = MongoClient(host)[database]
    
    return database[collection]

def store(collection, dictionary):
    collection.insert_one(dictionary)



test_dict = {
    "Hello": "Dict"
}



config = get_config(test=True)
print(get_url(config))
print(init_db(config))
store(init_db(config), test_dict)

# tickets = init_db(db_string, db, collection)
# tickets.insert_one(test_dict)





