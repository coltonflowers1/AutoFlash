document.addEventListener('DOMContentLoaded', function () {
    const decksContainer = document.getElementById('decks-editor');
    const addDeckForm = document.getElementById('addDeckForm'); // Assuming you have a form for adding decks
    const addDeckNameInput = document.getElementById("newSetName"); // Input for new deck's name

    // Function to fetch and display all decks
    function loadDecks() {
        fetch('/decks')
            .then(response => response.json())
            .then(decks => {
                decksContainer.innerHTML = ''; // Clear the container
                decks.forEach(deck => {
                    console.log(deck);
                    const deckDiv = document.createElement('div');
                    deckDiv.className = 'deck';

                    const deckNameSpan = document.createElement('span');
                    deckNameSpan.textContent = deck.name;
                    deckDiv.appendChild(deckNameSpan);
                    // Study button
                    const studyButton = document.createElement('button');
                    studyButton.textContent = 'Study';
                    studyButton.onclick = function () {
                        window.location.href = `/static/study/study.html?set=${deck._id}`;
                    };
                    deckDiv.appendChild(studyButton);
                    const editButton = document.createElement('button');
                    editButton.textContent = 'Edit';
                    editButton.onclick = function () {
                        window.location.href = `/static/edit_deck/edit_deck.html?deckId=${deck._id}`;
                    };
                    deckDiv.appendChild(editButton);

                    const deleteButton = document.createElement('button');
                    deleteButton.textContent = 'Delete';
                    deleteButton.onclick = function () {
                        deleteDeck(deck._id);
                    };
                    deckDiv.appendChild(deleteButton);

                    decksContainer.appendChild(deckDiv);
                });
            })
            .catch(error => console.error('Failed to load decks:', error));
    }

    // Function to delete a deck
    function deleteDeck(deckId) {
        fetch(`/decks/${deckId}`, { method: 'DELETE' })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                loadDecks(); // Reload decks after deletion
            })
            .catch(error => console.error('Failed to delete deck:', error));
    }

    // Event listener for adding a new deck
    addDeckForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const deckName = addDeckNameInput.value;
        fetch('/decks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: deckName })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                addDeckNameInput.value = ''; // Clear the input
                loadDecks(); // Reload decks after adding
            })
            .catch(error => console.error('Failed to add deck:', error));
    });

    loadDecks(); // Initial load of decks
});
