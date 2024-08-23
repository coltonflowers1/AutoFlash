# AutoFlash

This is a Flask application that allows users to manage and automatically generate flashcard decks.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/flashcard-deck-api.git
    ```
2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Start the Flask application:
    ```bash
    python restful_app.py
    ```

# Flashcard Deck API Documentation

 a RESTful API for managing flashcard decks.

## Endpoints

### GET /decks

Retrieves all flashcard decks from the database.

#### Response

A JSON array of flashcard decks. Each object in the array represents a flashcard deck and has the following properties:

- `id`: The ID of the flashcard deck.
- `name`: The name of the flashcard deck.
- `cards`: An array of flashcards in the deck. Each object in the array represents a flashcard and has the following properties:
    - `question`: The question of the flashcard.
    - `answer`: The answer of the flashcard.

### GET /decks/<id>

Retrieves a specific flashcard deck by its ID.

#### Parameters

- `id`: The ID of the flashcard deck.

#### Response

A JSON object that represents a flashcard deck and has the following properties:

- `id`: The ID of the flashcard deck.
- `name`: The name of the flashcard deck.
- `cards`: An array of flashcards in the deck. Each object in the array represents a flashcard and has the following properties:
    - `question`: The question of the flashcard.
    - `answer`: The answer of the flashcard.

### POST /decks/<id>

Creates a flashcard in a specific deck.

#### Parameters

- `id`: The ID of the flashcard deck.

#### Request Body

A JSON object that represents a flashcard and has the following properties:

- `question`: The question of the flashcard.
- `answer`: The answer of the flashcard.

#### Response

A JSON object that represents the created flashcard and has the following properties:

- `id`: The ID of the flashcard.
- `question`: The question of the flashcard.
- `answer`: The answer of the flashcard.

## Configuration

The application uses MongoDB for data storage. You can configure the MongoDB connection by setting the `MONGODB_URI` and `MONGODB_PASSWORD` environment variables.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)