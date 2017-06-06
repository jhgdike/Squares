/**
 * Created by firzen on 17-5-29.
 */
function send_start(tid)
{
    $.ajax({
        type: "POST",
        url: "/api/play/table/start/"+tid,
        dataType: "json",
        success: function(data){
            if(data["data"].is_start===true)
                window.alert("get started")
                gs=1;
        }
    });
}

function send_give_up(tid)
{
    $.ajax({
        type: "POST",
        url: "/api/play/table/quit/"+tid,
        dataType: "json",
        success: function(data){
            //window.clearInterval(t);
            alert("you gave up");
        }
    });
}