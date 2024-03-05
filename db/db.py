from os import getenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


### MonGo DB Stuff
uri = getenv("MONGO_URI")
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["harvestHub"]