function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

var swalert = {


    'alertError': function (msg) {
        swal('提示',msg,'error');
    },

    'alertInfo':function (msg) {
        swal('提示',msg,'warning');
    },

    'alertInfoWithTitle': function (title,msg) {
        swal(title,msg);
    },

    'alertSuccess':function (msg,confirmCallback) {
        args = {
            'title': '提示',
            'text': msg,
            'type': 'success',
        }
        swal(args,confirmCallback);
    }, 

    'alertSuccessWithTitle':function (title,msg) {
        swal(title,msg,'success');
    },

    'alertConfirm':function (params) {
        swal({
            'title': params['title'] ? params['title'] : '提示',
            'showCancelButton': true,
            'showConfirmButton': true,
            'type': params['type'] ? params['type'] : '',
            'confirmButtonText': params['confirmText'] ? params['confirmText'] : '确定',
            'cancelButtonText': params['cancelText'] ? params['cancelText'] : '取消',
            'text': params['msg'] ? params['msg'] : ''
        },function (isConfirm) {
            if(isConfirm){
                if(params['confirmCallback']){
                    params['confirmCallback']();
                }
            }else{
                if(params['cancelCallback']){
                    params['cancelCallback']();
                }
            }
        });
    },

    'alertOneInput': function (params) {
        swal({
            'title': params['title'] ? params['title'] : '请输入',
            'text': params['text'] ? params['text'] : '',
            'type':'input',
            'showCancelButton': true,
            'animation': 'slide-from-top',
            'closeOnConfirm': false,
            'showLoaderOnConfirm': true,
            'inputPlaceholder': params['placeholder'] ? params['placeholder'] : '',
            'confirmButtonText': params['confirmText'] ? params['confirmText'] : '确定',
            'cancelButtonText': params['cancelText'] ? params['cancelText'] : '取消',
        },function (inputValue) {
            if(inputValue === false) return false;
            if(inputValue === ''){
                swal.showInputError('输入框不能为空！');
                return false;
            }
            if(params['confirmCallback']){
                params['confirmCallback'](inputValue);
            }
        });
    },

    'alertNetworkError':function () {
        this.alertErrorToast('网络错误');
    },

    'alertInfoToast':function (msg) {
        this.alertToast(msg,'info');
    },

    'alertErrorToast':function (msg) {
        this.alertToast(msg,'error');
    },

    'alertSuccessToast':function (msg) {
        if(!msg){msg = '成功！';}
        this.alertToast(msg,'success');
    },

    'alertToast':function (msg,type) {
        swal({
            'title': msg,
            'text': '',
            'type': type,
            'showCancelButton': false,
            'showConfirmButton': false,
            'timer': 1000,
        });
    },
    'close': function () {
        swal.close();
    }

};

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

        var data = {};
        $("#form-bike-info").serializeArray().map(function(x) { data[x.name]=x.value });

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
					swalert.alertSuccessToast("Congratulations!Adding a bike information successfully!");

                    $("#form-bike-info").hide();

                    $("#form-bike-image").show();

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
					swalert.alertSuccessToast("Congratulations! Adding bike's images successfully!");
                    $(".bike-image-cons").append('<img src="' + resp.data.image_url +'">');
                } else {
                    alert(resp.errmsg);
                }
            }
        })
    })

})