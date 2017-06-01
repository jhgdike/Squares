/**
 * Created by firzen on 17-5-29.
 */
function send_start()
{
    $.ajax({
        type: "GET",
        url: "/view/api/play/table/ready",
        dataType: "json",
        success: function(data){
        }
    });
}

function send_give_up()
{
    $.ajax({
        type: "GET",
        url: "/view/api/play/table/give_up",
        dataType: "json",
        success: function(data){
            alert("you gave up");
        }
    });
}