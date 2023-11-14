
document.addEventListener('DOMContentLoaded', function() {
    const flashcardSetDropdown = document.getElementById('flashcardSetDropdown');
    const addFlashcardForm = document.getElementById('addFlashcardForm');
    const flashcardsList = document.getElementById('flashcardsList');
    const addFlashcardSection = document.getElementById('addFlashcardSection');
    const flashcardsListSection = document.getElementById('flashcardsListSection');
    const createSetForm = document.getElementById('createSetForm');
    const studySetButton = document.getElementById('studySetButton');
    
    let currentSetId = null;
    
    // Enable the study button only if a set is selected
    flashcardSetDropdown.addEventListener('change', function() {
        studySetButton.disabled = !this.value;
    });

    // Redirect to the study page with the selected set ID
    studySetButton.addEventListener('click', function() {
        const selectedSetId = flashcardSetDropdown.value;
        if (selectedSetId) {
            // Assuming you want to pass the selected set ID as a query parameter
            window.location.href = `/static/study/study.html?set=${selectedSetId}`;
        }
    });
    // Handle creating a new flashcard set
    createSetForm.onsubmit = function(event) {
        event.preventDefault();
        const setName = document.getElementById('newSetName').value;

        fetch('/create-flashcard-set', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ setName })
        })
        .then(response => response.text())
        .then(() => {
            loadFlashcardSets(); // Reload flashcard sets
            createSetForm.reset(); // Reset the form
        })
        .catch(error => console.error('Error:', error));
    };
    // Load flashcard sets into the dropdown
    function loadFlashcardSets() {
        fetch('/get-flashcard-sets')
        .then(response => response.json())
        .then(sets => {
            const dropdown = document.getElementById('flashcardSetDropdown');
            dropdown.innerHTML = ''; // Clear existing options

            sets.forEach(set => {
                const option = document.createElement('option');
                option.value = set.id; // Make sure 'id' matches the property in your data
                option.textContent = set.name; // And 'name' as well
                dropdown.appendChild(option);
            });
        })
        .catch(error => console.error('Error:', error));
}


    // Handle flashcard set selection
    flashcardSetDropdown.onchange = function() {
        currentSetId = this.value;
        if (currentSetId) {
            addFlashcardSection.style.display = 'block';
            flashcardsListSection.style.display = 'block';
            loadFlashcards(currentSetId);
        } else {
            addFlashcardSection.style.display = 'none';
            flashcardsListSection.style.display = 'none';
        }
    };

    // Load flashcards for the selected set
    // function loadFlashcards(setId) {
    //     fetch(`/get-flashcards/${setId}`)
    //     .then(response => response.json())
    //     .then(flashcards => {
    //         flashcardsList.innerHTML = ''; // Clear the list
    //         flashcards.forEach(card => {
    //             const listItem = document.createElement('li');
    //             listItem.textContent = `${card.frontText} - ${card.backText}`;
    //             // Optionally, add buttons for editing/deleting here
    //             // Create the delete button
    //             const deleteButton = document.createElement('button');
    //             deleteButton.textContent = 'X';
    //             deleteButton.onclick = function() {
    //                 deleteFlashcard(setId, card.cardId); // Assuming each card has a unique 'cardId'
    //                 loadFlashcards(setId)
    //             };

    //             listItem.appendChild(deleteButton);
    //             flashcardsList.appendChild(listItem);
    //         });
    //     })
    //     .catch(error => console.error('Error:', error));
    // }
    function loadFlashcards(setId) {
        // ... fetch logic ...
        fetch(`/get-flashcards/${setId}`)
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
                    deleteButton.onclick = function() {
                        deleteFlashcard(setId, card.cardId); // Assuming each card has a unique 'cardId'
                        loadFlashcards(setId)
                    };

                    listItem.appendChild(deleteButton);
            
                    flashcardsList.appendChild(listItem);
                })
            }
            )
    }
    

    // Handle adding a new flashcard
    addFlashcardForm.onsubmit = function(event) {
        event.preventDefault();
        const frontText = document.getElementById('frontText').value;
        const backText = document.getElementById('backText').value;

        fetch(`/add-flashcard/${currentSetId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ frontText, backText })
        })
        .then(response => response.text())
        .then(() => {
            loadFlashcards(currentSetId); // Reload flashcards
            addFlashcardForm.reset(); // Reset the form
        })
        .catch(error => console.error('Error:', error));
    };

    loadFlashcardSets(); // Initial load of flashcard sets
});

function deleteFlashcard(setId, cardId) {
    fetch(`/delete-flashcard/${setId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ cardId })
    })
    .then(response => response.json())
    .then(() => {
        loadFlashcards(setId); // Reload flashcards to update the list
    })
    .catch(error => console.error('Error:', error));
}
