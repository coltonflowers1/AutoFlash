document.addEventListener('DOMContentLoaded', function() {
   
    // let flashcards = [
    //     // Placeholder flashcards data
    //     { front: 'Front of card 1', back: 'Back of card 1' },
    //     { front: 'Front of card 2', back: 'Back of card 2' },
    //     // ... more flashcards ...
    // ];
    function getQueryParams() {
        const queryParams = new URLSearchParams(window.location.search);
        return {
            setId: queryParams.get('set'), // Assuming the parameter is named 'set'
        };
    }
    
    function fetchFlashcards(setId) {
        fetch(`/get-flashcards/${setId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(flashcards => {
            initializeFlashcardStudy(flashcards);
        })
        .catch(error => {
            console.error('Could not fetch flashcards:', error);
        });
    }
    
    function initializeFlashcardStudy(flashcards) {
        
        // Logic to display the first flashcard and set up navigation events
        // ... (similar to the logic you have in study.js already)
        // DOM elements
        let currentCardIndex = 0; // Index of the currently displayed flashcard
        const flashcardContainer = document.getElementById('flashcard-container');
        const frontSide = flashcardContainer.querySelector('.front-side');
        const backSide = flashcardContainer.querySelector('.back-side');
    
        // Function to display a flashcard
        function displayFlashcard(index) {
            const card = flashcards[index];
            frontSide.textContent = card.frontText;
            backSide.textContent = card.backText;
            frontSide.style.display = 'block';
            backSide.style.display = 'none';
        }
    
        // Function to flip the flashcard
        flashcardContainer.addEventListener('click', function() {
            const isFrontVisible = frontSide.style.display === 'block';
            frontSide.style.display = isFrontVisible ? 'none' : 'block';
            backSide.style.display = isFrontVisible ? 'block' : 'none';
        });
    
        // Navigate to the previous card
        document.getElementById('previous').addEventListener('click', function() {
            if (currentCardIndex > 0) {
                currentCardIndex--;
                displayFlashcard(currentCardIndex);
            }
        });
    
        // Navigate to the next card
        document.getElementById('next').addEventListener('click', function() {
            if (currentCardIndex < flashcards.length - 1) {
                currentCardIndex++;
                displayFlashcard(currentCardIndex);
            }
        });
    
        // Initialize the first flashcard
        displayFlashcard(currentCardIndex);
    }
    const { setId } = getQueryParams();
    if (setId) {
        fetchFlashcards(setId);
    } else {
        console.error('Set ID is required in query parameters.');
    }


});

