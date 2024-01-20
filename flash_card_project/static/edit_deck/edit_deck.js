
document.addEventListener('DOMContentLoaded', function () {
    // const flashcardSetDropdown = document.getElementById('flashcardSetDropdown');
    const addFlashcardForm = document.getElementById('addFlashcardForm');
    const flashcardsList = document.getElementById('flashcardsList');
    let currentSetId = getQueryParam('deckId')

    function getSetName(setId) {
        return fetch(`/decks/${encodeURIComponent(setId)}`)
            .then(response => response.json())
            .then(data => data.name) // assuming the response has a 'name' field
            .catch(error => console.error('Error:', error));
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

