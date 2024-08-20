import json
import os
from bottle import (
    post,
    put,
    request,
    response,
    run,
    route,
    delete,
    static_file,
)


from flash_card_project.mongodb_connect import db
from bson.objectid import ObjectId


decks_collection = db["decks"]

def parse_json(data):
    return json.dumps(data, default=str)

@route("/")
def serve_homepage():
    # print(static_file("index.html", root="static"))
    return static_file("index.html", root="static")


@route("/static/<filename:path>")
def serve_static(filename):
    return static_file(filename, root="./static")


@route("/decks", method="GET")
def get_decks():
  """
  Retrieves all decks from the database.

  Returns:
    list: A list of decks.
  """
  decks = list(decks_collection.find())
  return parse_json(decks)


@route("/decks/<id>")
def get_deck(id):
    """
    Retrieve a flashcard deck
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The id of the deck
    responses:
      200:
        description: Flashcard deck retrieved
      404:
        description: Flashcard deck not found
    """
    deck = decks_collection.find_one({"_id": ObjectId(id)})
    if deck:
        return parse_json(deck)
    response.status = 404
    return {"error": "Flashcard deck not found"}

@put("/decks")
def create_deck():
    """
    Create a new flashcard deck
    ---
    parameters:
      - in: body
        name: body
        schema:
          id: Deck
          required:
            - name
          properties:
            name:
            cards:
              type: array
              items:
                type: object
                properties:
                  question:
                    type: string
                  answer:
                    type: string
    """
    deck = request.json
    deck['cards'] = [{**card, '_id': ObjectId()} for card in deck.get('cards', [])]
    result = decks_collection.insert_one(deck)
    deck["_id"] = str(result.inserted_id)
    return {"message": "Flashcard deck created","_id": deck["_id"]}

# @put("/decks")
# def create_deck():
#     """
#     Create a new flashcard deck
#     ---
#     parameters:
#       - in: body
#         name: body
#         schema:
#           id: Deck
#           required:
#             - name
#           properties:
#             name:
#               type: string
#               description: The name of the deck
#             cards:
#               type: array
#               items:
#                 type: object
#                 properties:
#                   front:
#                     type: string
#                   back:
#                     type: string
#     responses:
#       200:
#         description: Flashcard deck created
#     """
#     deck = request.json
#     if deck.get("cards") is None:
#         deck["cards"] = []
#     result = decks_collection.insert_one(deck)
#     # deck["_id"] = str(result.inserted_id)
#     return parse_json(deck)


@post("/decks/<id>")
def update_deck(id):
    """
    Update a flashcard deck
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The id of the deck
      - in: body
        name: body
        schema:
          id: Deck
          properties:
            name:
              type: string
              description: The name of the deck
            cards:
              type: array
              items:
                type: object
                properties:
                  front:
                    type: string
                  back:
                    type: string
    responses:
      200:
        description: Flashcard deck updated
    """
    deck = request.json
    decks_collection.update_one({"_id": ObjectId(id)}, {"$deck": deck})
    return {"message": "Flashcard deck updated"}


@delete("/decks/<id>")
def delete_deck(id):
    """
    Delete a flashcard deck
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The id of the deck
    responses:
      200:
        description: Flashcard deck deleted
    """
    decks_collection.delete_one({"_id": ObjectId(id)})
    return {"message": "Flashcard deck deleted"}


@route("/decks/<id>/cards")
def get_cards_from_deck(id):
    """
    Retrieve all cards from a flashcard deck
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The id of the deck
    responses:
      200:
        description: A list of cards in the deck
      404:
        description: Flashcard deck not found
    """
    deck = decks_collection.find_one({"_id": ObjectId(id)})
    if deck:
        return parse_json(deck["cards"])
    response.status = 404
    return {"error": "Flashcard deck not found"}


@post("/decks/<id>/cards")
def add_card_to_deck(id):
    """
    Add a card to a deck
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The id of the deck
      - in: body
        name: body
        schema:
          id: Card
          required:
            - front
            - back
          properties:
            front:
              type: string
              description: The front for the card
            back:
              type: string
              description: The back for the card
    responses:
      200:
        description: Card added to deck
    """
    card = request.json
    # if not card or not 'front' in card or not 'back' in card:
    #     raise HTTPError(400, "Invalid input")

    deck = decks_collection.find_one({"_id": ObjectId(id)})
    # if not deck:
    #     raise HTTPError("",404, "Deck not found")

    card["_id"] = ObjectId()
    decks_collection.update_one({"_id": ObjectId(id)}, {"$push": {"cards": card}})
    return {"message": "Card added to flashcard deck"}


@delete("/decks/<deck_id>/cards/<card_id>")
def delete_card_from_deck(deck_id, card_id):
    """
    Delete a card from a deck
    ---
    parameters:
      - name: deck_id
        in: path
        type: string
        required: true
        description: The id of the deck
      - name: card_id
        in: path
        type: string
        required: true
        description: The id of the card
    responses:
      200:
        description: Card deleted from deck
    """
    result = decks_collection.update_one(
        {"_id": ObjectId(deck_id)}, {"$pull": {"cards": {"_id": ObjectId(card_id)}}}
    )
    assert result.modified_count == 1
    return {"message": "Card deleted from flashcard deck"}


@post("/decks/<deck_id>/cards/<card_id>")
def update_card_in_deck(deck_id, card_id):
    """
    Update a card in a deck
    ---
    parameters:
      - name: deck_id
        in: path
        type: string
        required: true
        description: The id of the deck
      - name: card_id
        in: path
        type: string
        required: true
        description: The id of the card
      - in: body
        name: body
        schema:
          id: Card
          required:
            - front
            - back
          properties:
            front:
              type: string
              description: The front for the card
            back:
              type: string
              description: The back for the card
    responses:
      200:
        description: Card updated in deck
    """
    card = request.json
    decks_collection.update_one(
        {"_id": ObjectId(deck_id), "cards.id": card_id}, {"$deck": {"cards.$": card}}
    )
    return {"message": "Card updated in flashcard deck"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    run(host="0.0.0.0", port=port, debug=True, reloader=True)
