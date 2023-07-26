from bson.json_util import dumps
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

# Connect to our database
db = client['to_do_api']

# Fetch our series collection
users = db['users']
tasks = db['tasks']
