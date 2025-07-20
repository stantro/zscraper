import time
from .packages.utils import *

if __name__ == "__main__":

    config = get_config()

    while True:

        response = request(config)

        response_json = convert_response(response)
        
        config['start'] = str(response_json['end_time'])

        tickets = change_key(response_json['tickets'])

        mongo_client = init_db(config)

        ticket_collection = get_collection(config, mongo_client)

        store(ticket_collection, tickets)

        close_db(mongo_client)

        time.sleep(30)