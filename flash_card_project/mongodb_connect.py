from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import datetime
import pprint
from bson.objectid import ObjectId
# Replace the placeholder with your Atlas connection string
uri = os.environ["MONGODB_URI"]

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


# for set in flashcard_sets.find():
#     # Check if the set has flashcards and they don't already have IDs
#     if 'flashcards' in set and (not set['flashcards'] or 'card_id' not in set['flashcards'][0]):
#         updated_flashcards = []

#         for card in set['flashcards']:
#             # Assign a unique ID to each flashcard
#             card['card_id'] = str(ObjectId())
#             updated_flashcards.append(card)

#         # Update the flashcard set with the new flashcards list
#         flashcard_sets.update_one(
#             {'_id': set['_id']},
#             {'$set': {'flashcards': updated_flashcards}}
#         )

flashcard_sets.update_one(
        {'_id': ObjectId("655077af056419ed221261dd")},
        {'$pull': {'flashcards': {'card_id': "655119cffb5e73c40568c303"}}}
    )
# new_posts = [
#     {
#         "author": "Mike",
#         "text": "Another post!",
#         "tags": ["bulk", "insert"],
#         "date": datetime.datetime(2009, 11, 12, 11, 14),
#     },
#     {
#         "author": "Eliot",
#         "title": "MongoDB is fun",
#         "text": "and pretty easy too!",
#         "date": datetime.datetime(2009, 11, 10, 10, 45),
#     },
# ]
# result = posts.insert_many(new_posts)
# result.inserted_ids
# post_id = posts.insert_one(post)
# print(post_id)

# pprint.pprint(posts.find_one())
# for post in posts.find():
#     pprint.pprint(post)
# for post in posts.find({"author": "Mike"}):
#     pprint.pprint(post)
result = flashcard_sets.find(
            {"_id": ObjectId("655077af056419ed221261dd")}
        )
for post in result:
    pprint.pprint(post)