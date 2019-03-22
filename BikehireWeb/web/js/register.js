function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function() {
    $("#inputUserName").focus(function(){
        $("#inputUsername-err").hide();
    });
    $("#inputEmail").focus(function(){
        $("#inputEmail-err").hide();
    });
    $("#inputPassword").focus(function(){
        $("#inputpassword-err").hide();
        $("#inputConfirmPassword-err").hide();
    });
    $("#confirmpassword").focus(function(){
        $("#inputConfirmPassword-err").hide();
    });


    $(".form-register").submit(function(e){

        e.preventDefault();
        alert("in the form");
        var UserName = $("#inputUserName").val();
        var Email = $("#inputEmail").val();
        var passwd = $("#inputPassword").val();
        var passwd2 = $("#confirmpassword").val();

        if (!UserName) {
            $("#inputUsername-err span").html("please input your Username");
            $("#inputUsername-err").show();
            return;
        }
        if (!Email) {
            $("#inputEmail-err span").html("please input your Email");
            $("#inputEmail-err").show();
            return;
        }
        if (!passwd) {
            $("#inputpassword-err span").html("please input your password!");
            $("#inputpassword-err").show();
            return;
        }
        if (passwd != passwd2) {
            $("#inputConfirmPassword-err span").html("Confirm password is inconsis");
            $("#inputConfirmPassword-err").show();
            return;
        }

        //  Call AJAX to send a registration request to the backend
        var req_data = {
            username: UserName,
            email: Email,
            password: passwd,
            password2: passwd2,
        };
        var req_json = JSON.stringify(req_data);
        $.ajax({
            url: "/api/v1.0/users",
            type: "post",
            data: req_json,
            contentType: "application/json",
            dataType: "json",
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            }, // Request header, put the csrf_token value in the request, to facilitate the backend CSRF to verify
            success: function (resp) {
                if (resp.errno == "0") {
                    // Successful registration, jump to the homepage
                    location.href = "/index.html";
                } else {
                    alert(resp.errmsg);
            }
            }
        })

    });
})