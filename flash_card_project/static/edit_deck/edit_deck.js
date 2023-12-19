
document.addEventListener('DOMContentLoaded', function () {
    // const flashcardSetDropdown = document.getElementById('flashcardSetDropdown');
    const addFlashcardForm = document.getElementById('addFlashcardForm');
    const flashcardsList = document.getElementById('flashcardsList');
    const autoPopSection = document.getElementById('AutoPopulate');
    let currentSetId = getQueryParam('deckId')

    function getSetName(setId) {
        return fetch(`/decks/${encodeURIComponent(setId)}`)
            .then(response => response.json())
            .then(data => data.name) // assuming the response has a 'name' field
            .catch(error => console.error('Error:', error));
    }
    // Get the generate button and autoPopSection elements
    const generateButton = document.getElementById('generate-button');
    // Event listener for the generate button
    generateButton.addEventListener('click', async () => {
        // Make a POST request to the provided URL
        let all_flashcards = fetch(`/decks/${currentSetId}/cards`)
                            .then(response => response.json())
                            .then(flashcards => {
                                console.log(flashcards)
                                return flashcards.map(flashcard => ({
                                    front_of_flashcard: flashcard.frontText, // Replace 'newKey1' and 'oldKey1' with your actual keys
                                    back_of_flashcard: flashcard.backText, // Replace 'newKey2' and 'oldKey2' with your actual keys
                                    // Add more keys if needed
                                  }));
                            })
                            .catch(error => console.error('Error:', error));
                            
        all_flashcards = await all_flashcards; // Wait for the flashcards to be fetched
        all_flashcards.sort(() => Math.random() - 0.5);
                // Get a random sample of 5 flashcards
        const flashcards = all_flashcards.slice(0, 5);
        console.log(flashcards);
        const response = await fetch('http://0.0.0.0:5002/generate_flashcard_with_examples', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({flashcards}),
        });

        // Parse the response as JSON and extract the new flashcard
        const flashcard = await response.json();
        const flashcardsSection = document.getElementById('autoPopulateflashcardsSection');
        // Create new elements for the front and back of the flashcard and set their text
        const listItem = document.createElement('li');
        // Create div for front text
        const frontDiv = document.createElement('div');
        frontDiv.classList.add('card-text');
        frontDiv.textContent = flashcard.front;

        // Create div for back text
        const backDiv = document.createElement('div');
        backDiv.classList.add('card-text');
        backDiv.textContent = flashcard.back;

        listItem.appendChild(frontDiv);
        listItem.appendChild(backDiv);

        listItem.addEventListener('click', function () {
            // add the flashcard to the flashcardsList
            addCard(flashcard.front, flashcard.back);
            // remove the flashcard from the autoPopulateflashcardsSection
            flashcardsSection.removeChild(listItem);
        });
        // Append the new flashcard to the autoPopSection
        flashcardsSection.appendChild(listItem);
    });
    function createAutoPopSection() {
        getSetName(currentSetId).then(currentSetName => {
            let num_flashcards = 15;
            
            autoPopSection.addEventListener('click', function () {
                fetch(`http://0.0.0.0:5002/generate_flashcards?topic=${encodeURIComponent(currentSetName)}&num_flashcards=${num_flashcards}`, { method: "GET", mode: 'cors' })
                    .then(response => response.json())
                    .then(data => {
                        const flashcardsSection = document.getElementById('autoPopulateflashcardsSection');
                        flashcardsSection.innerHTML = ''; // clear the section

                        data.forEach(flashcard => {
                            // Append both divs to the list item
                            // add the flashcard to the flashcardsList
                            const listItem = document.createElement('li');
                            // Create div for front text
                            const frontDiv = document.createElement('div');
                            frontDiv.classList.add('card-text');
                            frontDiv.textContent = flashcard.front;

                            // Create div for back text
                            const backDiv = document.createElement('div');
                            backDiv.classList.add('card-text');
                            backDiv.textContent = flashcard.back;

                            listItem.appendChild(frontDiv);
                            listItem.appendChild(backDiv);

                            listItem.addEventListener('click', function () {
                                // add the flashcard to the flashcardsList
                                addCard(flashcard.front, flashcard.back);
                                // remove the flashcard from the autoPopulateflashcardsSection
                                flashcardsSection.removeChild(listItem);
                            });

                            flashcardsSection.appendChild(listItem);
                        });
                    })
                    .catch(error => console.error('Error:', error));
            });
        });
    }

    function loadFlashcards(setId) {
        // ... fetch logic ...
        fetch(`/decks/${setId}/cards`)
            .then(response => response.json())
            .then(flashcards => {
                flashcardsList.innerHTML = ''; // Clear the list
                flashcards.forEach(card => {
                    const listItem = document.createElement('li');

                    // Create div for front text
                    const frontDiv = document.createElement('div');
                    frontDiv.classList.add('card-text');
                    frontDiv.textContent = card.frontText;

                    // Create div for back text
                    const backDiv = document.createElement('div');
                    backDiv.classList.add('card-text');
                    backDiv.textContent = card.backText;

                    // Append both divs to the list item
                    listItem.appendChild(frontDiv);
                    listItem.appendChild(backDiv);

                    // Append the delete button (not shown here for brevity)
                    const deleteButton = document.createElement('button');
                    deleteButton.textContent = 'X';
                    deleteButton.onclick = function () {
                        deleteFlashcard(setId, card._id); // Assuming each card has a unique 'cardId'
                        loadFlashcards(setId)
                    };

                    listItem.appendChild(deleteButton);

                    flashcardsList.appendChild(listItem);
                })
            }
            )
    }
    function deleteFlashcard(setId, cardId) {
        fetch(`/decks/${setId}/cards/${cardId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            // body: JSON.stringify({ cardId })
        })
            .then(response => response.text())
            .then(() => {
                loadFlashcards(setId); // Reload flashcards to update the list
            })
            .catch(error => console.error('Error:', error));
    }
    // Handle adding a new flashcard
    addFlashcardForm.onsubmit = function (event) {
        event.preventDefault();
        const frontText = document.getElementById('frontText').value;
        const backText = document.getElementById('backText').value;
        addCard(frontText, backText)
        addFlashcardForm.reset(); // Reset the form

        loadFlashcards(currentSetId)

        // loadFlashcardSets(); // Initial load of flashcard sets
    };
    createAutoPopSection();
    function addCard(frontText, backText) {
        fetch(`/decks/${currentSetId}/cards`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ frontText, backText })
        })
            .then(response => response.text())
            .then(() => {
                loadFlashcards(currentSetId); // Reload flashcards to update the list
            })
            .catch(error => console.error('Error:', error));
    }
    loadFlashcards(currentSetId); // Initial load of flashcard sets
});



function getQueryParam(param) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(param);
}

