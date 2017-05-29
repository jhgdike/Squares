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