from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient('localhost', 27017)

# Connect to our database
db = client['to_do_api']

# Fetch our series collection
users = db['users']
tasks = db['tasks']
