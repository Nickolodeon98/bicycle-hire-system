function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}


$(document).ready(function() {

    $("#password").focus(function(){
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function(){
        $("#password2-err").hide();
    });
	
	// add a customize function event for form submit
    $(".form-register").submit(function(e){
		//prevent browser auto submit 
        e.preventDefault();
		
        var username = $("#username").val();
        var passwd = $("#password").val();
        var passwd2 = $("#password2").val();
        if (!username) {
            $("#username-err span").html("请填写正确的用户名！");
            $("#username-err").show();
            return;
        } 
        if (!passwd) {
            $("#password-err span").html("请填写密码!");
            $("#password-err").show();
            return;
        }
        if (passwd != passwd2) {
            $("#password2-err span").html("两次密码不一致!");
            $("#password2-err").show();
            return;
        }
		
		//use ajax
		var req_data = {
			name: username
			password: passwd
			password2: passwd2
		}
		var req_json = JSON.stringify(req_data);
		$.ajax({
			url: "/api/v1.0/users",
			type: "post",
			data: req_json,
			contentType: "application/json",
			dataType: "json"
			success: function(resp){
				if(resp.errno=="0"){
					//register is success
					location.herf = "/index.html";
				}else{
					alert(resp.errmsq);
				}
			}
		})
    });
})