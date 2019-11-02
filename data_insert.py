import json
from pymongo import MongoClient
import os

COUNTRIES = ['Guinea', 'Liberia', 'Sierra_Leone']

if __name__ == '__main__':
    with open('db_auth.json') as json_file:
        auth_data = json.load(json_file)
        client = MongoClient(auth_data['client_string'])

    for country in COUNTRIES:
        db = client[country]
        path = "data/" + country
        for filename in os.listdir(path):
            with open(path + "/" + filename) as json_file:
                data = json.load(json_file)
                col = db[filename]
                col.insert_one(data)

    client.close()