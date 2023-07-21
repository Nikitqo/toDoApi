from bson.json_util import dumps
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

# Connect to our database
db = client['to_do_api']

# Fetch our series collection
users = db['users']
tasks = db['tasks']


def add_new_user(data, collection=users):
    return collection.insert_one(data)


def find_user(mail, collection=users):
    json_data = dumps(collection.find({"email": mail}))
    return json_data