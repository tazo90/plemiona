$(document).ready(function()
{    
    var time=0;        
    
    var produced = parseInt($("#time_taken").text().split(' ')[0])
    var jednostka = $("#time_taken").text().split(' ')[1]

    window.setInterval(function() {                    
        time += 1;          
        if (time % 10 == 0) {       
            produced += 30;
            $("#time_taken").text("");
            $("#time_taken").text(produced + ' ' + jednostka);
        }       
    }, 1000);
});

