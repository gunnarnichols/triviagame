$(document).ready(function () {
    //read and keep user selection
    var user_selection = [];

    user_selection = $(this);
    console.log(user_selection[0].id + ' clicked!');
    $('#category').text(user_selection[0].id);
            
    console.log($('#category').text())
    category = $('#category').text()

    data= { 
            'category' : category,
    }

     // clicking on any of the options will return value to user_selection
     $('.option').on('click', Selection);
     // clicking on any of the options will return value to user_selection
    function Selection() {
            user_selection = $(this);
            console.log(user_selection[0].id + ' clicked!');
            $('#category').text(user_selection[0].id);
            
            console.log($('#category').text())
            category = $('#category').text()

            data= { 
                    'category' : category,
                }

         
    } 

    $('#startgame').on('click', submit);

    function submit(){
        $.ajax({
            type : "POST",
            url : "/category/select",
            data: JSON.stringify(data, null, '\t'),
            contentType: 'application/json;charset=UTF-8',
            success: function(result) {
                console.log(result);
                //store results in browsers local storage
                localStorage.setItem("gameID", JSON.stringify(result[0]['gameID']));
                
                //reiderect to the game page
                window.location.href = '/game';
            }
        });
    }

});
