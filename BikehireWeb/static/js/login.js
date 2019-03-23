function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#inputUserName").focus(function(){
        $("#inputUsername-err").hide();
    });
    $("#inputPassword").focus(function(){
        $("#inputpassword-err").hide();
    });
    $("#form-login").submit(function(e){
        e.preventDefault();
        Username = $("#inputUserName").val();
        passwd = $("#password").val();
        if (!Username) {
            $("#inputUserName-err span").html("请填写正确的手机号！");
            $("#inputUsername-err").show();
            return;
        } 
        if (!passwd) {
            $("#inputpassword-err span").html("请填写密码!");
            $("#inputpassword-err").show();
            return;
        }
        // 将表单的数据存放到对象data中
        var data = {
            username: Username,
            password: passwd
        };
        // 将data转为json字符串
        var jsonData = JSON.stringify(data);
        $.ajax({
            url:"/api/v1.0/sessions",
            type:"post",
            data: jsonData,
            contentType: "application/json",
            dataType: "json",
            headers:{
                "X-CSRFToken":getCookie("csrf_token")
            },
            success: function (data) {
                if (data.errno == "0") {
                    // 登录成功，跳转到主页
                    location.href = "/";
                }
                else {
                    // 其他错误信息，在页面中展示
                    $("#password-err span").html(data.errmsg);
                    $("#password-err").show();
                }
            }
        });
    });
})