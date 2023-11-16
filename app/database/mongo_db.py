import motor.motor_asyncio


client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
# client = MongoClient('localhost', 27017) // not async client

# Connect to our database
db = client['to_do_api']

# Fetch our series collection
users = db['users']
tasks = db['tasks']
boards = db['boards']
