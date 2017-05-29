/**
 * Created by firzen on 17-5-27.
 */
var board=new Array(20);
for(let i=0;i<20;i++)
{
    board[i]=new Array(20);
    for(let j=0;j<20;j++)
    {
        board[i][j]=-1;
    }
}

function take_place(chess_order,x,y)
{
    let cx=Math.floor((x-600)/40);
    let cy=Math.floor(y/40);
    let temp=new Array(2);
    for(let i=0;i<player.chess[chess_order].num;i++)
    {
        let cood=cal(player.chess[chess_order].rotate,player.chess[chess_order].reverse,player.chess[chess_order].charax[i],player.chess[chess_order].charay[i]);
        temp[0]=cx+cood[0];
        temp[1]=cy-cood[1];
        if(temp[0]<0 || temp[0]>19 || temp[1]<0 || temp[1]>19)
            return false;
        if(board[temp[0]][temp[1]]===-1)
        {
            if(temp[0]>0)
                if(board[temp[0]-1][temp[1]]===pla_num)
                    return false;
            if(temp[0]<19)
                if(board[temp[0]+1][temp[1]]===pla_num)
                    return false;
            if(temp[1]>0)
                if(board[temp[0]][temp[1]-1]===pla_num)
                    return false;
            if(temp[1]<19)
                if(board[temp[0]][temp[1]+1]===pla_num)
                    return false;
        }
        else
        {
            return false;
        }
    }
    let det=0;
    if(step===0)
    {
        user=pla_num;
        pla_num===2?user=3:0;
        pla_num===3?user=2:0;
        let my=Math.floor(user/2);
        let mx=user%2;
        for(let i=0;i<player.chess[chess_order].num;i++)
        {
            let cood=cal(player.chess[chess_order].rotate,player.chess[chess_order].reverse,player.chess[chess_order].charax[i],player.chess[chess_order].charay[i]);
            temp[0]=cx+cood[0];
            temp[1]=cy-cood[1];
            if (temp[0]===mx*19 && temp[1]===my*19)
                det=1;
        }
    }
    else
    {
        for (let i = 0; i < player.chess[chess_order].num; i++)
        {
            let cood=cal(player.chess[chess_order].rotate,player.chess[chess_order].reverse,player.chess[chess_order].charax[i],player.chess[chess_order].charay[i]);
            temp[0]=cx+cood[0];
            temp[1]=cy-cood[1];
            try
            {
                if (board[temp[0] - 1][temp[1] - 1] === pla_num || board[temp[0] - 1][temp[1] + 1] === pla_num || board[temp[0] + 1][temp[1] + 1] === pla_num || board[temp[0] + 1][temp[1] - 1] === pla_num)
                    det = 1;
            }
            catch (err)
            {
                0;
            }
        }
    }
    if(det===0)
        return false;
    for (let i = 0; i < player.chess[chess_order].num; i++)
    {
        let cood=cal(player.chess[chess_order].rotate,player.chess[chess_order].reverse,player.chess[chess_order].charax[i],player.chess[chess_order].charay[i]);
        temp[0]=cx+cood[0];
        temp[1]=cy-cood[1];
        board[temp[0]][temp[1]]=pla_num;
    }
    return true;
}
