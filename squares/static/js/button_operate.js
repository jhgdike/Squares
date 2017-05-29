/**
 * Created by firzen on 17-5-28.
 */
function rota(chessnum)
{
    player.chess[chessnum].erase();
    player.chess[chessnum].rotate++;
    player.chess[chessnum].rotate=player.chess[chessnum].rotate%4;
    player.chess[chessnum].plot();
    player.chess[chessnum].plotted_flag--;
}

function reve(chessnum)
{
    player.chess[chessnum].erase();
    player.chess[chessnum].reverse++;
    player.chess[chessnum].rotate=(4-player.chess[chessnum].rotate)%4;
    player.chess[chessnum].reverse=player.chess[chessnum].reverse%2;
    player.chess[chessnum].plot();
    player.chess[chessnum].plotted_flag--;
}

function reco(chessnum)
{
    player.chess[chessnum].erase();
    player.chess[chessnum].rotate=0;
    player.chess[chessnum].reverse=0;
    player.chess[chessnum].posix=player.chess[chessnum].orix;
    player.chess[chessnum].posiy=player.chess[chessnum].oriy;
    player.chess[chessnum].plot();
    player.chess[chessnum].plotted_flag--;
    select_flag=-1;
}