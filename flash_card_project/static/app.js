document.addEventListener('DOMContentLoaded', function () {
    const decksContainer = document.getElementById('decks-editor');
    const addDeckForm = document.getElementById('createDeckForm'); // Assuming you have a form for adding decks
    const addDeckInput = document.getElementById('deckName'); // Assuming you have a form for adding decks
    const autoGenerateDeckButton = document.getElementById('autoCreateDeckButton');
    const blankCreateDeckButton = document.getElementById('blankCreateDeckButton');
    // Function to fetch and display all decks
    $("#edit-button").on('click', function() {
        $(".topic-selection").hide();
        $("#topic-input").show();
    });
    // Event listener for adding a new deck
    addDeckForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const deckName = addDeckInput.value;
        fetch('/decks', {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: deckName })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                addDeckInput.value = ''; // Clear the input
                loadDecks(); // Reload decks after adding
            })
            .catch(error => console.error('Failed to add deck:', error));
    });
    function loadDecks() {
        fetch('/decks')
            .then(response => response.json())
            .then(decks => {
                decksContainer.innerHTML = ''; // Clear the container
                decks.forEach(deck => {
                    console.log(deck);
                    const deckSection = document.createElement('section');
                    deckSection.className = 'deck';

                    const deckNameSpan = document.createElement('span');
                    deckNameSpan.textContent = deck.name;
                    deckSection.appendChild(deckNameSpan);
                    // Study button
                    const studyButton = document.createElement('button');
                    studyButton.textContent = 'Study';
                    studyButton.onclick = function () {
                        window.location.href = `/static/study/study.html?set=${deck._id}`;
                    };
                    studyButton.classList.add('study-button')
                    // deckSection.appendChild(studyButton);
                    const editButton = document.createElement('button');
                    editButton.textContent = 'Edit';
                    editButton.onclick = function () {
                        window.location.href = `/static/edit_deck/edit_deck.html?deckId=${deck._id}`;
                    };
                    editButton.classList.add('edit-button')
                    // deckSection.appendChild(editButton);

                    // Create a new div for the button container
                    const buttonContainer = document.createElement('section');
                    buttonContainer.classList.add('button-container');

                    // Append the buttons to the button container
                    buttonContainer.appendChild(studyButton);
                    buttonContainer.appendChild(editButton);

                    // Append the button container to the deckSection
                    deckSection.appendChild(buttonContainer);

                    const deleteButton = document.createElement('button');
                    deleteButton.textContent = 'x';
                    deleteButton.classList.add('delete-button')
                    deleteButton.onclick = function () {
                        deleteDeck(deck._id);
                    };
                    deckSection.appendChild(deleteButton);

                    decksContainer.appendChild(deckSection);
                });
            })
            .catch(error => console.error('Failed to load decks:', error));
    }
        // Event listener for adding a new deck
    // addDeckForm.addEventListener('submit', function (event) {
    //     event.preventDefault();
    //     const deckName = addNameInput.value;
    //     fetch('/decks', {
    //         method: 'POST',
    //         headers: { 'Content-Type': 'application/json' },
    //         body: JSON.stringify({ name: deckName })
    //     })
    //         .then(response => {
    //             if (!response.ok) {
    //                 throw new Error('Network response was not ok');
    //             }
    //             addDeckInput.value = ''; // Clear the input
    //             loadDecks(); // Reload decks after adding
    //         })
    //         .catch(error => console.error('Failed to add deck:', error));
    // });

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

    autoGenerateDeckButton.addEventListener('click', function () {
        $("#deck-creation-section").show();
        $("#autocreate").show();
        $("#blankCreate").hide();

    });
    blankCreateDeckButton.addEventListener('click', function () {
        $("#deck-creation-section").show();
        $("#autocreate").hide();
        $("#blankCreate").show();
    });

    $("#autocomplete").on('input', function() {
        var request = $(this).val();
        if (request.length < 2) return;
    
        $.ajax({
            url: "https://en.wikipedia.org/w/api.php",
            dataType: "jsonp",
            data: {
                'action': "opensearch",
                'format': "json",
                'search': request
            },
            success: function(data) {
                // Update the list of concepts
                var conceptList = $("#concept-list");
                conceptList.empty();
                data[1].forEach(function(item) {
                    var listItem = $("<li>").text(item);
                    listItem.on('click', function() {
                        $("#autocomplete").val(item);
                        conceptList.empty();
                        $("#topic-input").hide();
                        $("#topic").text(item);
                        $(".topic-selection").show();
                    });
                    conceptList.append(listItem);
                });
            }
        });
    });
    $.ajaxSetup({
        contentType: "application/json; charset=utf-8"
      });
    
    $('#generate-button').click(function() {
        // Show the progress-wheel
        $("#status").text("Creating Deck...");
        $('#status').show();
        var topic = $('#autocomplete').val(); // get the topic from the input field
        var num_flashcards = $('#number-input').val(); // get the number of flashcards from the input field
        $.post("http://0.0.0.0:5002/start_operation", JSON.stringify({
            topic: topic,
            num_flashcards: num_flashcards
          }), function(data){
            var task_id = data.task_id;
            var intervalID = setInterval(function(){
                $.get("http://0.0.0.0:5002/operation_status/" + task_id, function(data){
                    if (data.state === 'PENDING') {
                        $("#status").text("Creating Deck...");
                    } else if (data.state === 'PROGRESS') {
                        $("#status").text("Creating Deck: " + "(" + data.progress + "/" + num_flashcards + " created)");
                        
                        var radius = $("#progress-wheel .path").attr('r');
                        var circumference = 2 * Math.PI * radius;
                        $("#progress-wheel .path").css('stroke-dasharray', circumference);
                        var percent_done = data.progress / num_flashcards;
                        var offset = circumference - percent_done * circumference;
                        $("#progress-wheel .path").css('stroke-dashoffset', offset);
                        $('#progress-wheel').show();
                    } else if (data.state === 'SUCCESS') {
                        // $("#status").text("Operation completed successfully!");
                        $("#status").text("Your '" + topic + "' deck has been created! Check your decks page to study it.");
                        var deck_id = data.deck_id;
                        console.log(deck_id)
                        $('#progress-wheel').hide();
                        // Display the study and edit buttons
                        // var studyButton = $('<button>').text('Study').click(function() {
                        //     window.location.href = `/static/study/study.html?set=${deck_id}`;
                        // });
                        // $('#flashcards').append(studyButton);
                        // var editButton = $('<button>').text('Edit').click(function() {
                        //         window.location.href = `/static/edit_deck/edit_deck.html?deckId=${deck_id}`;
                        // });
    
                        clearInterval(intervalID);
                        loadDecks(); // Reload decks after adding
                    } else {
                        $("#status").text("Operation failed: " + data.status);
                        clearInterval(intervalID);
                    }
                });
            }, 1000);
        });
    });
    
    // Event listener for adding a new deck
    // addDeckForm.addEventListener('submit', function (event) {
    //     event.preventDefault();
    //     const deckName = addDeckNameInput.value;
    //     fetch('/decks', {
    //         method: 'POST',
    //         headers: { 'Content-Type': 'application/json' },
    //         body: JSON.stringify({ name: deckName })
    //     })
    //         .then(response => {
    //             if (!response.ok) {
    //                 throw new Error('Network response was not ok');
    //             }
    //             addDeckNameInput.value = ''; // Clear the input
    //             loadDecks(); // Reload decks after adding
    //         })
    //         .catch(error => console.error('Failed to add deck:', error));
    // });

    loadDecks(); // Initial load of decks
});