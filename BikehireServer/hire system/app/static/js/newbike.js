function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // get locations info from server
    $.get("/api/v1.0/locations", function (resp) {
        if (resp.errno == "0") {
            var locations = resp.data;
            var html = template("locations-tmpl", {locations: locations})
            $("#location-id").html(html);

        } else {
            alert(resp.errmsg);
        }

    }, "json");

    $("#form-bike-info").submit(function (e) {
        e.preventDefault();

        // 处理表单数据
        var data = {};
        $("#form-bike-info").serializeArray().map(function(x) { data[x.name]=x.value });

        // 向后端发送请求
        $.ajax({
            url: "/api/v1.0/bikes/info",
            type: "post",
            contentType: "application/json",
            data: JSON.stringify(data),
            dataType: "json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            success: function (resp) {
                if (resp.errno == "4101") {
                    // user not login
                    location.href = "/login.html";
                } else if (resp.errno == "0") {
                    // 隐藏基本信息表单
                    $("#form-bike-info").hide();
                    // 显示图片表单
                    $("#form-bike-image").show();
                    // 设置图片表单中的bike_id
                    $("#bike-id").val(resp.data.bike_id);
                } else {
                    alert(resp.errmsg);
                }
            }
        })

    });
    $("#form-bike-image").submit(function (e) {
        e.preventDefault();
        $(this).ajaxSubmit({
            url: "/api/v1.0/bikes/image",
            type: "post",
            dataType: "json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token"),
            },
            success: function (resp) {
                if (resp.errno == "4101") {
                    location.href = "/login.html";
                } else if (resp.errno == "0") {
                    $(".bike-image-cons").append('<img src="' + resp.data.image_url +'">');
                } else {
                    alert(resp.errmsg);
                }
            }
        })
    })

})