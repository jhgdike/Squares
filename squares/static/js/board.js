/**
 * Created by firzen on 17-5-24.
 */
var drawing=document.getElementById("drawing");
var turnWarn = 0;
if(drawing.getContext)
{
    var context=drawing.getContext("2d");
    // the chessboard
    context.fillStyle="rgba(127,0,127,1)";
    context.fillRect(600,0,800,800);
    context.strokeStyle="green";
    for(var i=0;i<20;i++)
    {
        for(var j=0;j<20;j++)
        {
            context.strokeRect(600+i*40,j*40,40,40);
        }
    }
    context.fillStyle="black";
    // all the chesses are on the left\
}

function ask_for_fresh(tid) {
    if(gs===0)
    {
        $.ajax(
            {
                type: "GET",
                url: "/api/play/table/observe/" + tid,
                //async: false,
                dataType: "json",
                success: function (data) {
                    if (data["data"].is_start===true) {
                        gs = 1;
                        console.log(gs);
                        window.alert("get started");
                    }
                }
            });
    }
    else {
        if (time_to_move === 0) {
            $.ajax(
                {
                    type: "GET",
                    url: "/api/play/table/observe/" + tid,
                    //async: false,
                    dataType: "json",
                    success: function (data) {
                        for (var i = 0; i < 20; i++) {
                            for (var j = 0; j < 20; j++) {
                                context.fillStyle = pid2col[data["data"].squares[i][j]];
                                context.fillRect(600 + i * 40, j * 40, 40, 40);
                                context.strokeRect(600 + i * 40, j * 40, 40, 40);
                                board[i][j] = data["data"].squares[i][j]
                            }
                        }
                        if (data["data"].turn == data["data"].player_n) {
                            time_to_move = 1;
                            if (turnWarn == 0) {
                                turnWarn = 1;
                                window.alert("time to move");
                            }
                        }
                    }
                });
        }
    }
}

function waiting_for_turn(tid) {
    $.ajax(
        {
            type: "GET",
            url: "/api/play/table/observe/"+tid,
            dataType: "json",
            success: function (data) {
                for(var i=0;i<20;i++)
                {
                    for(var j=0;j<20;j++)
                    {
                        context.fillStyle=pid2col[data.player_n];
                        context.fillRect(600+i*40,j*40,40,40);
                        context.strokeRect(600+i*40,j*40,40,40);
                        board[i][j]=data.squares[i][j];
                    }
                }
                if(data["data"].turn==data["data"].player_n)
                    time_to_move=1;
            }
        });
}