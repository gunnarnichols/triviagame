$(document).ready(function () {

    //keep options
    var option1;
    var option2;
    var option3;
    var option4;
    //keep answer location
    var answer_location;
    //keep user selection
    var user_selection = [];
    // count how many attempt used
    var attempt_counter = 0;
    //Make Add score to Leader board form appear

    $('#submitScore').click(function () {
        console.log('clicked!');
        $('#cover-caption').slideToggle("slow");
    });

    // clicking on any of the options and buttons
    var opt = $('.option');
    opt.on('click',Selection);
    function Selection() {
        //get user selection
        user_selection = $(this);
        console.log(user_selection[0]+'clicked!');
    }

    //TODO: subtract lives if neccesary
    //TODO: Assign points

    //Display new question
    $('#next').on('click', DisplayNewQuestion);
    //Check if selection is correct
    var sub = $('#submit');
    sub.on('click', Submit);
    //------------------------------------
    //SELECT A NEW RANDOM QUESTION
    //TODO: Replace max number with number of questions come backend
    function DisplayNewQuestion() {
        sub.on('click', Submit);
        // replace the changed color back.
        $('.option').css('color', 'black')
        var max_number = 50;
        var test_int = Math.floor(Math.random() * max_number);
        $.ajax({
            dataType: 'json',
            type: 'GET',
            url: '/question/' + test_int,
            success: function (data) {
                // Log data on front end
                console.log(typeof data);
                console.log(data);

                //replace front end ui with NEW data from server
                $('#question').text(data[1]['Question']);
                option1 = $('#option_1').text("A: " + data[2]['Answer']);

                option2 = $('#option_2').text("B: " + data[3]['Option_1']);

                option3 = $('#option_3').text("C: " + data[4]['Option_2']);

                option4 = $('#option_4').text("D: " + data[5]['Option_3']);

                answer_location = data[6]['Answer_Location'];
            }
        });
    }

    // return answer, count attempts
    function Submit() {

        sub.off('click', Submit);

        //console.log(user_selection);
        //console.log(Answer());
        if (user_selection[0] == Answer()) {
            // change answer color to green
            $(Answer()).css('color', 'green');


            // score function can be added score++ in this if function

        } else {
            // change user_selection color to red, and answer to green
            $(user_selection).css('color', 'red');
            $(Answer()).css('color', 'green');

            // attempt counter count one chance
            attempt_counter++;


            // score function can be added score-- in here.

        }

        // when 3 attempts, game over, only allow to submit score.
        if (attempt_counter >= 3) {
            alert("GameOver!" + "Score shows up here");
            $('#next').detach();
            $('#submit').detach();
        }
    }

    // function for checking which option is the answer
    function Answer() {
        if (answer_location == 1) {
            q_answer = option_1;
        } else if (answer_location == 2) {
            q_answer = option_2;
        } else if (answer_location == 3) {
            q_answer = option_3;
        } else {
            q_answer = option_4;
        }
        console.log(q_answer);
        return q_answer;
    }
});
