/**
 * Created by firzen on 17-5-27.
 */
function myBrowser(){
    var userAgent = navigator.userAgent; //取得浏览器的userAgent字符串
    var isOpera = userAgent.indexOf("Opera") > -1;
    if (isOpera) {
        return "Opera"
    } //判断是否Opera浏览器
    if (userAgent.indexOf("Firefox") > -1) {
        return "FF";
    } //判断是否Firefox浏览器
    if (userAgent.indexOf("Chrome") > -1){
        return "Chrome";
    }
    if (userAgent.indexOf("Safari") > -1) {
        return "Safari";
    } //判断是否Safari浏览器
    if (userAgent.indexOf("compatible") > -1 && userAgent.indexOf("MSIE") > -1 && !isOpera) {
        return "IE";
    } //判断是否IE浏览器
}

function get_mouse_position(x,y)
{
    console.log(time_to_move, gs);
    if (time_to_move == 1 && gs==1) {
        let cx;
        let cy;
        if ((x >= 600 && x <= 1400) && (y >= 0 && y <= 800)) {//on board
            cx = Math.floor((x - 600) / 40);
            cy = Math.floor(y / 40);
            if (select_flag >= 0) {
                let flag = take_place(playern, select_flag, x, y);
                if (flag) {
                    player.chess[select_flag].erase();
                    player.chess[select_flag].posix = cx * 40 + 600;
                    player.chess[select_flag].posiy = cy * 40;
                    player.chess[select_flag].plot();
                    player.chess[select_flag].used = 1;
                    console.log(select_flag);
                    $.ajax({
                        type: "POST",
                        url: "/api/play/table/step/"+tid,
                        data: {
                            schema_id: select_flag,
                            p_x: cx,
                            p_y: cy,
                            rotate: player.chess[select_flag].rotate,
                            symmetry: player.chess[select_flag].reverse
                        },
                        dataType: "json",
                        success: function (data) {
                            if(data["success"]===false) {
                                window.alert(data["error"]);
                                reco(select_flag);
                            }
                            else {
//                                window.alert("moved");
                                time_to_move = 0;
                            }
                        }
                    });
                    select_flag = -1;
                    step++;
                }
            }
        }
        else if (x >= 20 && x <= 580 && y >= 20 && y <= 780) {//on plate
            if (select_flag >= 0) {
                console.log('select_flag >= 0', select_flag);
                0;
            }
            else {
                for (let i = 0; i < 21; i++) {
                    if (player.chess[i].used) {
                        console.log(i, "used");
                        continue;
                    }
                    for (let j = 0; j < player.chess[i].num; j++) {
                        let judge = ((player.chess[i].last_pox + player.chess[i].charax[j] * 40) <= x);
                        judge = (judge && (x <= (player.chess[i].last_pox + player.chess[i].charax[j] * 40 + 40)));
                        judge = (judge && ((player.chess[i].last_poy - player.chess[i].charay[j] * 40) <= y));
                        judge = (judge && (y <= (player.chess[i].last_poy - player.chess[i].charay[j] * 40 + 40)));
                        console.log('judge', judge);
                        if (judge === true) {
                            console.log(select_flag)
                            select_flag = i;
                            console.log('select_flag', i);
                            player.chess[i].erase();
                            player.chess[i].posix = 1600;
                            player.chess[i].posiy = 200;
                            player.chess[i].plot();
                            player.chess[i].plotted_flag--;
                            button_flag = 1;
                            break;
                        }
                    }
                    if (select_flag >= 0)
                        break;
                }
            }
        }
    }
}

