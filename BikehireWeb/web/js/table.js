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

    $("#form-house-info").submit(function (e) {
        e.preventDefault();

        var data = {};
        $("#form-house-info").serializeArray().map(function(x) { data[x.name]=x.value });

        var facility = [];
        $(":checked[name=facility]").each(function(index, x){facility[index] = $(x).val()});

        data.facility = facility;

        $.ajax({
            url: "/api/v1.0/houses/info",
            type: "post",
            contentType: "application/json",
            data: JSON.stringify(data),
            dataType: "json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            success: function (resp) {
                if (resp.errno == "4101") {
                    location.href = "/login.html";
                } else if (resp.errno == "0") {
                    // Hide basic information forms
                    $("#form-house-info").hide();
                    // Display Picture Form
                    $("#form-house-image").show();
                    // Set house_id in the picture form
                    $("#house-id").val(resp.data.house_id);
                } else {
                    alert(resp.errmsg);
                }
            }
        })

    });

})