function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $.get("/api/v1.0/bikes", function (resp) {
        if (resp.errno == "0") {
            var bikes = resp.data.bikes;
            var html = template("bike-tmpl", {bikes: bikes})
            $("#bike-info").html(html);

        } else {
            alert(resp.errmsg);
        }

    }, "json");


})