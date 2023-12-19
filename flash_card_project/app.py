# import os
# from bottle import (
#     post,
#     put,
#     request,
#     response,
#     run,
#     delete,
#     route,
#     static_file,
#     template,
# )
# import json

# import bson
# from flash_card_project.mongodb_connect import db
# from bson.objectid import ObjectId

# flashcard_sets_collection = db["flashcard_sets"]


# @route("/")
# def serve_homepage():
#     # print(static_file("index.html", root="static"))
#     return static_file("index.html", root="static")


# @route("/static/<filename:path>")
# def serve_static(filename):
#     return static_file(filename, root="./static")


# # @post("/upload-flashcards")
# # def upload_flashcards():
# #     """
# #     Endpoint to upload a named set of flashcards to MongoDB.

# #     This endpoint accepts a POST request with a JSON payload containing a named set of flashcards.
# #     The JSON object must have a "set name" and an array of flashcards, each with "front text" and "back text".

# #     Request Format:
# #         - JSON object with a "set name" and a "flashcards" array.
# #         - Example: {"set name": "Geography", "flashcards": [{"front text": "Capital of France", "back text": "Paris"}, ...]}

# #     Response:
# #         - Success message if the flashcard set is saved to MongoDB.
# #         - Error message with a 400 status for invalid JSON or incorrect format.

# #     MongoDB:
# #         - Flashcard sets are saved to a collection named 'flashcard_sets'.
# #         - Each document represents a named set of flashcards.
# #     """

# #     try:
# #         data = request.json

# #         if (
# #             not isinstance(data, dict)
# #             or "set name" not in data
# #             or not isinstance(data.get("flashcards"), list)
# #         ):
# #             response.status = 400
# #             return "Invalid format for flashcard set"

# #         # Check if each flashcard has the required fields
# #         if not all(
# #             "front text" in card and "back text" in card for card in data["flashcards"]
# #         ):
# #             response.status = 400
# #             return "Invalid format for flashcards"

# #         # Insert the flashcard set into MongoDB
# #         result = flashcard_sets_collection.insert_one(data)

# #         return f"Flashcard set '{data['set name']}' uploaded successfully. Document ID: {result.inserted_id}"

# #     except json.JSONDecodeError:
# #         response.status = 400
# #         return "Invalid JSON"


# @post("/add-deck")
# def add_deck():
#     try:
#         data = request.json
#         new_deck_name = data.get("name")
#         if not new_deck_name:
#             response.status = 400
#             return "Deck name is required."

#         # Check if the deck already exists
#         if flashcard_sets_collection.find_one({"name": new_deck_name}):
#             response.status = 409
#             return "Deck with this name already exists."

#         new_deck = {"name": new_deck_name, "flashcards": []}
#         result = flashcard_sets_collection.insert_one(new_deck)
#         return json.dumps({"id": str(result.inserted_id)})
#     except Exception as e:
#         response.status = 500
#         return str(e)


# @route("/get-all-decks")
# def get_all_decks():
#     try:
#         decks = flashcard_sets_collection.find({}, {"_id": 1, "name": 1})
#         decks_list = [{"id": str(deck["_id"]), "name": deck["name"]} for deck in decks]
#         return json.dumps(decks_list)
#     except Exception as e:
#         response.status = 500
#         return str(e)


# @route("/flashcard-set/<set_id>")
# def flashcard_set_page(set_id):
#     set_info = fetch_set_info(set_id)  # Implement this function to fetch set details
#     cards = fetch_cards_for_set(
#         set_id
#     )  # Implement this function to fetch cards for the set

#     return template("flashcard_set.tpl", set_name=set_info["name"], cards=cards)
#     # Retrieve the specific flashcard set using set_id
#     # Render and return the page for this flashcard set


# def fetch_set_info(set_id):
#     """
#     Fetches information about a specific flashcard set from the database.

#     :param set_id: The unique identifier of the flashcard set.
#     :return: A dictionary containing information about the flashcard set.
#     """

#     # Assuming set_id is a unique identifier for the flashcard set.
#     # Adjust the query if your identifier is different (e.g., a name or a MongoDB ObjectId).
#     set_info = flashcard_sets_collection.find_one({"_id": ObjectId(set_id)})
#     if set_info:
#         # Optionally, you can transform the set_info here before returning it.
#         # For example, removing fields that should not be exposed.
#         return set_info
#     else:
#         # Return a default value or raise an error if the set is not found.
#         return {"name": "Unknown", "id": set_id}


# def fetch_cards_for_set(set_id):
#     """
#     Fetches all flashcards belonging to a specific set from the database.

#     :param set_id: The unique identifier of the flashcard set.
#     :return: A list of dictionaries, each representing a flashcard.
#     """
#     try:
#         # Fetch the specific set. Adjust the field names as per your database schema.
#         set_data = flashcard_sets_collection.find_one({"_id": ObjectId(set_id)})

#         if set_data and "flashcards" in set_data:
#             # Return the list of flashcards
#             return [
#                 {
#                     "frontText": set["front text"],
#                     "backText": set["back text"],
#                     "cardId": set["card_id"],
#                 }
#                 for set in set_data["flashcards"]
#             ]
#         else:
#             # Return an empty list if the set is not found or has no flashcards
#             return []
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return []


# @post("/add-flashcard/<set_id>")
# def add_flashcard(set_id):
#     """
#     Endpoint to add a flashcard to an existing set.

#     The request must include the set name and the flashcard data ("front text" and "back text").

#     Request Format:
#         - JSON object with "set name", "front text", and "back text".
#         - Example: {"set name": "Geography", "front text": "Capital of Germany", "back text": "Berlin"}

#     Response:
#         - Success or error message.
#     """
#     data = request.json

#     # Check if 'data' is a dictionary
#     if not isinstance(data, dict):
#         response.status = 400
#         return "Invalid request format"

#     # Validate input
#     if not all(key in data for key in ["frontText", "backText"]):
#         response.status = 400
#         return "Missing required flashcard data"

#     # Add flashcard to the set
#     # result = flashcard_sets_collection.update_one(
#     #     {"_id": ObjectId(set_id)},
#     #     {
#     #         "$push": {
#     #             "flashcards": {
#     #                 "front text": data["frontText"],
#     #                 "back text": data["backText"],
#     #             }
#     #         }
#     #     },
#     # )
#     result = _add_flashcard(set_id, data["frontText"], data["backText"])

#     if result.modified_count:
#         return "Flashcard added successfully"
#     else:
#         return "Flashcard set not found"


# @route("/get-flashcards/<set_id>")
# def get_flashcards(set_id):
#     """
#     Endpoint to retrieve all flashcards.

#     Returns a JSON list of all flashcards in the database.
#     Each flashcard set is represented as a dictionary.
#     """
#     # Fetch all flashcards for the specified set
#     flashcards = fetch_cards_for_set(set_id)

#     # Return the flashcards as JSON
#     return json.dumps(flashcards)


# @route("/get-deck-name/<set_id>")
# def get_flashcard_name(set_id):
#     """
#     Endpoint to retrieve all flashcards.

#     Returns a JSON list of all flashcards in the database.
#     Each flashcard set is represented as a dictionary.
#     """
#     # Fetch all flashcards for the specified set
#     info = fetch_set_info(set_id)

#     # Return the flashcards as JSON
#     return json.dumps({"name": info["name"]})


# @delete("/delete-flashcard/<set_id>")
# def delete_flashcard(set_id):
#     """
#     Endpoint to delete a flashcard from a set.

#     The request must include the set name and the flashcard data to be deleted.

#     Request Format:
#         - JSON object with "set name", "front text", and "back text".
#         - Example: {"set name": "Geography", "front text": "Capital of Italy", "back text": "Rome"}

#     Response:
#         - Success or error message.
#     """
#     # Retrieve the flashcard identifier from the request
#     data = request.json

#     if not isinstance(data, dict):
#         response.status = 400
#         return "Invalid request format"

#     flashcard_id = data.get("cardId")

#     print(data)

#     if not flashcard_id:
#         return "Flashcard ID is required", 400

#     try:
#         # Assuming each flashcard is a document in a 'flashcards' collection
#         result = flashcard_sets_collection.update_one(
#             {"_id": ObjectId(set_id)},
#             {"$pull": {"flashcards": {"card_id": flashcard_id}}},
#         )

#         if result.modified_count:
#             return "Flashcard deleted successfully"
#         else:
#             return "Flashcard not found or already deleted", 404
#     except Exception as e:
#         return str(e), 500


# @put("/edit-flashcard/<set_id>")
# def edit_flashcard(set_id):
#     """
#     Endpoint to edit an existing flashcard in a set.

#     The request must include the set name, the original flashcard data, and the new data.

#     Request Format:
#         - JSON object with "set name", "original front text", "original back text", "new front text", and "new back text".
#         - Example: {"set name": "Geography", "original front text": "Capital of Germany", "original back text": "Berlin", "new front text": "Capital of Italy", "new back text": "Rome"}

#     Response:
#         - Success or error message.
#     """
#     data = request.json

#     if not isinstance(data, dict):
#         response.status = 400
#         return "Invalid request format"

#     flashcard_id = data.get("cardId")
#     new_front_text = data.get("frontText")
#     new_back_text = data.get("backText")

#     if not all([flashcard_id, new_front_text, new_back_text]):
#         return "Missing required flashcard data", 400
#     try:
#         # Assuming each flashcard is a document in a 'flashcards' collection
#         result = flashcard_sets_collection.update_one(
#             {"_id": set_id, "flashcards.card_id": flashcard_id},
#             {
#                 "$set": {
#                     "flashcards.$.front_text": new_front_text,
#                     "flashcards.$.back_text": new_back_text,
#                 }
#             },
#         )
#         if result.modified_count:
#             return "Flashcard updated successfully"
#         else:
#             return "Flashcard not found", 404
#     except Exception as e:
#         return str(e), 500


# def _add_flashcard(set_id, front_text, back_text):
#     card_id = bson.ObjectId()  # Generates a new unique ObjectId
#     new_card = {
#         "card_id": str(card_id),
#         "front text": front_text,
#         "back text": back_text,
#     }

#     # Add the new card to the specified set
#     result = flashcard_sets_collection.update_one(
#         {"_id": ObjectId(set_id)}, {"$push": {"flashcards": new_card}}
#     )

#     return result


# @delete("/delete-deck/<deck_id>")
# def delete_deck(deck_id):
#     try:
#         # Convert deck_id from string to ObjectId, if necessary
#         result = flashcard_sets_collection.delete_one({"_id": ObjectId(deck_id)})

#         if result.deleted_count:
#             return "Deck deleted successfully."
#         else:
#             response.status = 404
#             return "Deck not found."
#     except Exception as e:
#         response.status = 500
#         return str(e)


# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 8080))
#     run(host="0.0.0.0", port=port, debug=True)
