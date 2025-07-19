from requests.auth import HTTPBasicAuth
from pymongo import MongoClient
import configparser
import requests
import os
import json

def get_config(test=False):

    root = os.getcwd()
    path = root + "/zscraper/config.ini"

    config = configparser.ConfigParser()
    config.read_file(open(path))

    return config['DEFAULT'] if not test else config['TEST']
    

def request(config):
    
    subdomain, start = config['subdomain'], config['start']
    url = f"https://{subdomain}.zendesk.com/api/v2/incremental/tickets?start_time={start}"

    email, token = config['email'], config['token']
    auth = HTTPBasicAuth(f"{email}/token", token)
    
    
    headers =  {
        "Content-Type": "application/json"
    }

    response = requests.request(
        "GET",
        url,
        auth=auth,
        headers=headers
    )

    print(response.status_code)
    return response.text

def convert_response(response):

    return json.loads(response)

def change_key(list):
    
    for dict in list:
        dict['zendesk_id'] = dict.pop('id')

    return list

def init_db(config):
    
    host = config['host']

    client = MongoClient(host)
    
    return client

def get_collection(config, client):

    database, collection = config['database'], config['collection']

    database = client[database]

    return database[collection]

def store(collection, list):
    
    collection.insert_many(list)

def close_db(client):
    
    client.close()






