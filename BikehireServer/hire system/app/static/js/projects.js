function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // 向后端获取城区信息
    $.get("/api/v1.0/bikes", function (resp) {
        if (resp.errno == "4001") {
            var bikes = resp;
            var html = template("bike-tmpl", {bikes: bikes})
            $("#bike-info").html(html);

        } else {
            alert(resp.errmsg);
        }

    }, "json");


    });