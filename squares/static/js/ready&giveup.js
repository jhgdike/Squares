/**
 * Created by firzen on 17-5-29.
 */
function ask_for_fresh(tid) {
    $.ajax(
        {
            type: "GET",
            url: "/view/api/play/table/observe/tid",
            dataType: "json",
            success: function (data) {
                data[]
            }
        });
}