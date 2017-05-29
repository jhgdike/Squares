/**
 * Created by firzen on 17-5-24.
 */
var chesses=document.getElementById("chesses");
let Chess=
    {
        createNew: function (color)
        {
            chess={};
            chess.color=color;
            chess.num=0;              //number of small square contains.
            //the first square set as (0,0);charax and charay mark the shift of other squares.
            chess.orix=0;
            chess.oriy=0;
            chess.posix=0;
            chess.posiy=0;
            chess.last_pox=0;
            chess.last_poy=0;
            chess.plotted_flag=0;
            chess.charax=new Array(4);
            chess.charay=new Array(4);
            for(let i=0;i<4;i++)
            {
                chess.charax[i]=chess.charay[i]=0;
            }
            chess.rotate=0;           //times of being rotated for 90 degree (0,1,2,3).
            chess.reverse=0;          //whether be reversed (0,1).
            chess.used=0;             //whether be used (0,1).
            chess.draw=draw;          //draw this chess.the upper left of the first square is at (startx,starty).
            chess.plot=plot;
            chess.erase=erase;
            function plot()
            {
                let context=chesses.getContext("2d");
                // the chess layer
                context.fillStyle=this.color;
                context.strokeStyle="green";
                let coor=new Array(2);
                for(let i=0;i<this.num;i++)
                {
                    coor = cal(this.rotate,this.reverse,this.charax[i],this.charay[i]);
                    context.fillRect(this.posix+coor[0]*40,this.posiy-coor[1]*40,40,40);
                    context.strokeRect(this.posix+coor[0]*40,this.posiy-coor[1]*40,40,40);
                }
                this.plotted_flag++;
                this.last_pox=this.posix;
                this.last_poy=this.posiy;
                return "plotted";
            }
            function erase()
            {
                let context=chesses.getContext("2d");
                let coor=new Array(2);
                if(this.plotted_flag===1)
                {
                    for (let i = 0; i < this.num; i++)
                    {
                        coor=cal(this.rotate,this.reverse,this.charax[i],this.charay[i]);
                        context.clearRect(this.posix + coor[0] * 40-5, this.posiy - coor[1]* 40-5, 50, 50);
                    }
                }
                else if(this.plotted_flag>1)
                {
                    for (let i = 0; i < this.num; i++)
                    {
                        coor=cal(this.rotate,this.reverse,this.charax[i],this.charay[i]);
                        context.clearRect(this.posix + coor[0] * 40, this.posiy - coor[1] * 40, 40, 40);
                    }
                }
            }
            function draw()
            {
                let context=chesses.getContext("2d");
                // the chess layer
                context.fillStyle=this.color;
                context.strokeStyle="green";
                if(this.plotted_flag===1)
                {
                    for (let i = 0; i < this.num; i++)
                    {
                        context.clearRect(this.last_pox + this.charax[i] * 40-5, this.last_poy - this.charay[i]* 40-5, 50, 50);
                    }
                }
                else if(this.plotted_flag>1)
                {
                    for (let i = 0; i < this.num; i++)
                    {
                        context.clearRect(this.last_pox + this.charax[i] * 40, this.last_poy - this.charay[i] * 40, 40, 40);
                    }
                }
                for(let i=0;i<this.num;i++)
                {
                    context.fillRect(this.posix+this.charax[i]*40, this.posiy-this.charay[i]*40, 40, 40);
                    context.strokeRect(this.posix+this.charax[i]*40, this.posiy-this.charay[i]*40, 40, 40);
                }
                this.plotted_flag++;
                this.last_pox=this.posix;
                this.last_poy=this.posiy;
                return "plotted";
            }
            return chess;
        }
    };

function create_chesses(color,player) {
    player.chess=new Array(21);
    for(let i=0;i<21;i++)
        player.chess[i]=Chess.createNew(color);
    let j=0;
    //chess 0
    // .
    player.chess[j].num=1;
    player.chess[j].posix=player.chess[j].orix=20;
    player.chess[j].posiy=player.chess[j].oriy=20;
    player.chess[j].plot();
    j++;
    //chess 1
    // ..
    player.chess[j].num=2;
    player.chess[j].charax[1]=1;
    player.chess[j].charay[1]=0;
    player.chess[j].posix=player.chess[j].orix=100;
    player.chess[j].posiy=player.chess[j].oriy=20;
    player.chess[j].plot();
    j++;
    //chess 2
    // ...
    player.chess[j].num=3;
    player.chess[j].charax[1]=1;
    player.chess[j].charay[1]=0;
    player.chess[j].charax[2]=2;
    player.chess[j].charay[2]=0;
    player.chess[j].posix=player.chess[j].orix=220;
    player.chess[j].posiy=player.chess[j].oriy=20;
    player.chess[j].plot();
    j++;
    //chess 3
    //  .
    // ..
    player.chess[j].num=3;
    player.chess[j].charax[1]=1;
    player.chess[j].charay[1]=0;
    player.chess[j].charax[2]=1;
    player.chess[j].charay[2]=1;
    player.chess[j].posix=player.chess[j].orix=380;
    player.chess[j].posiy=player.chess[j].oriy=60;
    player.chess[j].plot();
    j++;
    //chess 4
    // ....
    player.chess[j].num=4;
    player.chess[j].charax[1]=1;
    player.chess[j].charay[1]=0;
    player.chess[j].charax[2]=2;
    player.chess[j].charay[2]=0;
    player.chess[j].charax[3]=3;
    player.chess[j].charay[3]=0;
    player.chess[j].posix=player.chess[j].orix=20;
    player.chess[j].posiy=player.chess[j].oriy=100;
    player.chess[j].plot();
    j++;
    //chess 5
    //  .
    //  .
    // ..
    player.chess[j].num=4;
    player.chess[j].charax[1]=1;
    player.chess[j].charay[1]=0;
    player.chess[j].charax[2]=1;
    player.chess[j].charay[2]=1;
    player.chess[j].charax[3]=1;
    player.chess[j].charay[3]=2;
    player.chess[j].posix=player.chess[j].orix=220;
    player.chess[j].posiy=player.chess[j].oriy=180;
    player.chess[j].plot();
    j++;
    //chess 6
    //  .
    // ...
    player.chess[j].num=4;
    player.chess[j].charax[1]=1;
    player.chess[j].charay[1]=0;
    player.chess[j].charax[2]=1;
    player.chess[j].charay[2]=1;
    player.chess[j].charax[3]=2;
    player.chess[j].charay[3]=0;
    player.chess[j].posix=player.chess[j].orix=340;
    player.chess[j].posiy=player.chess[j].oriy=180;
    player.chess[j].plot();
    j++;
    //chess 7
    // ..
    // ..
    player.chess[j].num=4;
    player.chess[j].charax[1]=1;
    player.chess[j].charay[1]=0;
    player.chess[j].charax[2]=1;
    player.chess[j].charay[2]=1;
    player.chess[j].charax[3]=0;
    player.chess[j].charay[3]=1;
    player.chess[j].posix=player.chess[j].orix=500;
    player.chess[j].posiy=player.chess[j].oriy=60;
    player.chess[j].plot();
    j++;
    //chess 8
    //  ..
    // ..
    player.chess[j].num=4;
    player.chess[j].charax[1]=1;
    player.chess[j].charay[1]=0;
    player.chess[j].charax[2]=1;
    player.chess[j].charay[2]=1;
    player.chess[j].charax[3]=2;
    player.chess[j].charay[3]=1;
    player.chess[j].posix=player.chess[j].orix=20;
    player.chess[j].posiy=player.chess[j].oriy=220;
    player.chess[j].plot();
    j++;
    //chess 9
    // .....
    player.chess[j].num=5;
    player.chess[j].charax[1]=1;
    player.chess[j].charay[1]=0;
    player.chess[j].charax[2]=2;
    player.chess[j].charay[2]=0;
    player.chess[j].charax[3]=3;
    player.chess[j].charay[3]=0;
    player.chess[j].charax[4]=4;
    player.chess[j].charay[4]=0;
    player.chess[j].posix=player.chess[j].orix=140;
    player.chess[j].posiy=player.chess[j].oriy=260;
    player.chess[j].plot();
    j++;
    //chess 10
    //  .
    //  .
    //  .
    // ..
    player.chess[j].num=5;
    player.chess[j].charax[1]=1;
    player.chess[j].charay[1]=0;
    player.chess[j].charax[2]=1;
    player.chess[j].charay[2]=1;
    player.chess[j].charax[3]=1;
    player.chess[j].charay[3]=2;
    player.chess[j].charax[4]=1;
    player.chess[j].charay[4]=3;
    player.chess[j].posix=player.chess[j].orix=500;
    player.chess[j].posiy=player.chess[j].oriy=260;
    player.chess[j].plot();
    j++;
    //chess 11
    //  .
    //  .
    // ..
    // .
    player.chess[j].num=5;
    player.chess[j].charax[1]=0;
    player.chess[j].charay[1]=1;
    player.chess[j].charax[2]=1;
    player.chess[j].charay[2]=1;
    player.chess[j].charax[3]=1;
    player.chess[j].charay[3]=2;
    player.chess[j].charax[4]=1;
    player.chess[j].charay[4]=3;
    player.chess[j].posix=player.chess[j].orix=20;
    player.chess[j].posiy=player.chess[j].oriy=420;
    player.chess[j].plot();
    j++;
    //chess 12
    //  .
    // ..
    // ..
    player.chess[j].num=5;
    player.chess[j].charax[1]=1;
    player.chess[j].charay[1]=0;
    player.chess[j].charax[2]=1;
    player.chess[j].charay[2]=1;
    player.chess[j].charax[3]=1;
    player.chess[j].charay[3]=2;
    player.chess[j].charax[4]=0;
    player.chess[j].charay[4]=1;
    player.chess[j].posix=player.chess[j].orix=140;
    player.chess[j].posiy=player.chess[j].oriy=420;
    player.chess[j].plot();
    j++;
    //chess 13
    // ..
    //  .
    // ..
    player.chess[j].num=5;
    player.chess[j].charax[1]=1;
    player.chess[j].charay[1]=0;
    player.chess[j].charax[2]=1;
    player.chess[j].charay[2]=1;
    player.chess[j].charax[3]=1;
    player.chess[j].charay[3]=2;
    player.chess[j].charax[4]=0;
    player.chess[j].charay[4]=2;
    player.chess[j].posix=player.chess[j].orix=260;
    player.chess[j].posiy=player.chess[j].oriy=420;
    player.chess[j].plot();
    j++;
    //chess 14
    //  .
    // ....
    player.chess[j].num=5;
    player.chess[j].charax[1]=1;
    player.chess[j].charay[1]=0;
    player.chess[j].charax[2]=1;
    player.chess[j].charay[2]=1;
    player.chess[j].charax[3]=2;
    player.chess[j].charay[3]=0;
    player.chess[j].charax[4]=3;
    player.chess[j].charay[4]=0;
    player.chess[j].posix=player.chess[j].orix=380;
    player.chess[j].posiy=player.chess[j].oriy=340;
    player.chess[j].plot();
    j++;
    //chess 15
    //  .
    //  .
    // ...
    player.chess[j].num=5;
    player.chess[j].charax[1]=1;
    player.chess[j].charay[1]=0;
    player.chess[j].charax[2]=1;
    player.chess[j].charay[2]=1;
    player.chess[j].charax[3]=1;
    player.chess[j].charay[3]=2;
    player.chess[j].charax[4]=2;
    player.chess[j].charay[4]=0;
    player.chess[j].posix=player.chess[j].orix=20;
    player.chess[j].posiy=player.chess[j].oriy=580;
    player.chess[j].plot();
    j++;
    //chess 16
    //   .
    //   .
    // ...
    player.chess[j].num=5;
    player.chess[j].charax[1]=1;
    player.chess[j].charay[1]=0;
    player.chess[j].charax[2]=2;
    player.chess[j].charay[2]=0;
    player.chess[j].charax[3]=2;
    player.chess[j].charay[3]=1;
    player.chess[j].charax[4]=2;
    player.chess[j].charay[4]=2;
    player.chess[j].posix=player.chess[j].orix=180;
    player.chess[j].posiy=player.chess[j].oriy=580;
    player.chess[j].plot();
    j++;
    //chess 17
    //   .
    //  ..
    // ..
    player.chess[j].num=5;
    player.chess[j].charax[1]=1;
    player.chess[j].charay[1]=0;
    player.chess[j].charax[2]=1;
    player.chess[j].charay[2]=1;
    player.chess[j].charax[3]=2;
    player.chess[j].charay[3]=1;
    player.chess[j].charax[4]=2;
    player.chess[j].charay[4]=2;
    player.chess[j].posix=player.chess[j].orix=340;
    player.chess[j].posiy=player.chess[j].oriy=580;
    player.chess[j].plot();
    j++;
    //chess 18
    //  ..
    //  .
    // ..
    player.chess[j].num=5;
    player.chess[j].charax[1]=1;
    player.chess[j].charay[1]=0;
    player.chess[j].charax[2]=1;
    player.chess[j].charay[2]=1;
    player.chess[j].charax[3]=1;
    player.chess[j].charay[3]=2;
    player.chess[j].charax[4]=2;
    player.chess[j].charay[4]=2;
    player.chess[j].posix=player.chess[j].orix=20;
    player.chess[j].posiy=player.chess[j].oriy=740;
    player.chess[j].plot();
    j++;
    //chess 19
    //  .
    //  ..
    // ..
    player.chess[j].num=5;
    player.chess[j].charax[1]=1;
    player.chess[j].charay[1]=0;
    player.chess[j].charax[2]=1;
    player.chess[j].charay[2]=1;
    player.chess[j].charax[3]=1;
    player.chess[j].charay[3]=2;
    player.chess[j].charax[4]=2;
    player.chess[j].charay[4]=1;
    player.chess[j].posix=player.chess[j].orix=180;
    player.chess[j].posiy=player.chess[j].oriy=740;
    player.chess[j].plot();
    j++;
    //chess 20
    //  .
    // ...
    /// .  this line is y=-1
    player.chess[j].num=5;
    player.chess[j].charax[1]=1;
    player.chess[j].charay[1]=0;
    player.chess[j].charax[2]=1;
    player.chess[j].charay[2]=1;
    player.chess[j].charax[3]=1;
    player.chess[j].charay[3]=-1;
    player.chess[j].charax[4]=2;
    player.chess[j].charay[4]=0;
    player.chess[j].posix=player.chess[j].orix=340;
    player.chess[j].posiy=player.chess[j].oriy=700;
    player.chess[j].plot();
    j++;

    return "created";
}

function cal(rotate,reverse,x,y)
{
    let xx=0;
    let yy=0;
    let temp;
    if(reverse)
    {
        xx=-1*x;
        yy=y;
    }
    else
    {
        xx=x;
        yy=y;
    }
    for(let i=0;i<rotate;i++)
    {
        temp=xx;
        xx=-1*yy;
        yy=temp;
    }
    let arr=new Array(2);
    arr[0]=xx;
    arr[1]=yy;
    return arr;
}