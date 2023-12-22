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
    $('#progress-wheel').show();
    $('#status').show();
    $('#flashcards').empty();
    var topic = $('#autocomplete').val(); // get the topic from the input field
    var num_flashcards = $('#number-input').val(); // get the number of flashcards from the input field
    $.post("http://localhost:5002/start_operation", JSON.stringify({
        topic: topic,
        num_flashcards: num_flashcards
      }), function(data){
        var task_id = data.task_id;
        var intervalID = setInterval(function(){
            $.get("http://localhost:5002/operation_status/" + task_id, function(data){
                if (data.state === 'PENDING') {
                    $("#status").text("Operation is pending...");
                } else if (data.state === 'PROGRESS') {
                    $("#status").text("Operation is in progress: " + data.progress + "%");
                    var radius = $("#progress-wheel .path").attr('r');
                    var circumference = 2 * Math.PI * radius;
                    $("#progress-wheel .path").css('stroke-dasharray', circumference);
                    var offset = circumference - data.progress / 100 * circumference;
                    $("#progress-wheel .path").css('stroke-dashoffset', offset);
                } else if (data.state === 'SUCCESS') {
                    // $("#status").text("Operation completed successfully!");
                    // if ('result' in data) {
                    //     $("#result").text("Result: " + data.result);
                    // }
                        // Remove all existing flashcards
                    
                    $('#status').hide();
                    $('#progress-wheel').hide();
                    var flashcards = data.result;
                    for (var i = 0; i < flashcards.length; i++) {
                        var flashcard = flashcards[i];
                        // Create a new div for each flashcard
                        var flashcardDiv = $('<div class="flashcard">');
                        // Create a new div for the question and append it to the flashcard div
                        var questionDiv = $('<div class="question">').text('Question: ' + flashcard.front);
                        flashcardDiv.append(questionDiv);
                        // Create a new div for the answer and append it to the flashcard div
                        var answerDiv = $('<div class="answer">').text('Answer: ' + flashcard.back);
                        flashcardDiv.append(answerDiv);
                        // Append the new div to the #flashcards div
                        $('#flashcards').append(flashcardDiv);
                    }
                    clearInterval(intervalID);
                } else {
                    $("#status").text("Operation failed: " + data.status);
                    clearInterval(intervalID);
                }
            });
        }, 1000);
    });
});

$("#edit-button").on('click', function() {
    $(".topic-selection").hide();
    $("#topic-input").show();
});