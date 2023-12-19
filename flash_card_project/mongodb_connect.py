from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import datetime
import pprint
from bson.objectid import ObjectId
# Replace the placeholder with your Atlas connection string
# uri = os.environ["MONGODB_URI"]
MONGO_PASSWORD = os.environ["MONGO_PASSWORD"]
uri = f"mongodb+srv://cflowers:{MONGO_PASSWORD}@cluster0.ycnoox1.mongodb.net/"
# Set the Stable API version when creating a new client
client = MongoClient(uri, server_api=ServerApi('1'))
                          
# Send a ping to confirm a successful connection
db = client["flashcard_database"]
flashcard_sets = db["flashcard_sets"]

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

