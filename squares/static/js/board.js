/**
 * Created by firzen on 17-5-24.
 */
var drawing=document.getElementById("drawing");
if(drawing.getContext)
{
    var context=drawing.getContext("2d");
    // the chessboard
    context.fillStyle="rgba(127,0,127,0.5)";
    context.fillRect(600,0,800,800);
    context.strokeStyle="green";
    for(var i=0;i<20;i++)
    {
        for(var j=0;j<20;j++)
        {
            context.strokeRect(600+i*40,j*40,40,40);
        }
    }
    // all the chesses are on the left\
}

function ask_for_fresh(tid) {
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
                    }
                }
                if(data.is_started==1)
                {
                    alert("game started!!");
                    gs=1;
                    window.clearInterval(t);
                }
            }
        });
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
                if(data.turn==data.player_n)
                    time_to_move=1;
            }
        });
}