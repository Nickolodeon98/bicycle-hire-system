function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function updateFilterDateDisplay() {
    var startDate = $("#start").val();
    var endDate = $("#end").val();
    var $filterDateTitle = $(".filter-title-bar>.filter-title").children("input").eq(0);
    if (startDate) {
        var text = startDate.substr(5) + "/" + endDate.substr(5);
        $filterDateTitle.html(text);
    } else {
        $filterDateTitle.html("入住日期");
    }
}



function updateHouseData(action) {
    var areaId = $(".filter-area>li.active").attr("area-id");
    if (undefined == areaId) areaId = "";
    var startDate = $("#start").val();
    var endDate = $("#end").val();
    var sortKey = $(".filter-sort>li.active").attr("sort-key");
    var params = {
        aid:areaId,
        sd:startDate,
        ed:endDate,
        sk:sortKey,
        p:next_page
    };
    $.get("/api/v1.0/houses", params, function(resp){
        house_data_querying = false;
        if ("0" == resp.errno) {
            if (0 == resp.data.total_page) {
                $(".house-list").html("error");
            } else {
                total_page = resp.data.total_page;
                if ("renew" == action) {
                    cur_page = 1;
                    $(".house-list").html(template("house-list-tmpl", {houses:resp.data.houses}));
                } else {
                    cur_page = next_page;
                    $(".house-list").append(template("house-list-tmpl", {houses: resp.data.houses}));
                }
            }
        }
    })
}




$(document).ready(function(){
	var queryData = decodeQuery();
    var startDate = queryData["sd"];
    var endDate = queryData["ed"];
    $("#start").val(startDate);
    $("#end").val(endDate);
    updateFilterDateDisplay();
	
	
    $.get("/api/v1.0/bikes", function (resp) {
        if (resp.errno == "0") {
            var bikes = resp.data.bikes;
            var html = template("bike-tmpl", {bikes: bikes})
            $("#bike-info").html(html);

        } else {
            alert(resp.errmsg);
        }

    }, "json");
	



    $("#location-search").click(function (e) {
        e.preventDefault();

		$.get("/api/v1.0/locations", function (resp) {
			if (resp.errno == "0") {
				var locations = resp.data;
				var html = template("locations-tmpl", {locations: locations})
				$("#location-id").html(html);

			} else {
				alert(resp.errmsg);
			}

		}, "json");
    });
	
	
	
	var queryData = decodeQuery();
    var startDate = queryData["sd"];
    var endDate = queryData["ed"];
    $("#start").val(startDate);
    $("#end").val(endDate);
    updateFilterDateDisplay();
    var areaName = queryData["aname"];
    if (!areaName) areaName = "location";
    $(".filter-title-bar>.filter-title").eq(1).children("span").eq(0).html(areaName);


    $.get("/api/v1.0/areas", function(data){
        if ("0" == data.errno) {

            var areaId = queryData["aid"];

            if (areaId) {
                for (var i=0; i<data.data.length; i++) {

                    areaId = parseInt(areaId);
                    if (data.data[i].aid == areaId) {
                        $(".filter-area").append('<li area-id="'+ data.data[i].aid+'" class="active">'+ data.data[i].aname+'</li>');
                    } else {
                        $(".filter-area").append('<li area-id="'+ data.data[i].aid+'">'+ data.data[i].aname+'</li>');
                    }
                }
            } else {

                for (var i=0; i<data.data.length; i++) {
                    $(".filter-area").append('<li area-id="'+ data.data[i].aid+'">'+ data.data[i].aname+'</li>');
                }
            }
            updateHouseData("renew");

        }
    });




    var $filterItem = $(".filter-item-bar>.filter-item");
    $(".filter-title-bar").on("click", ".filter-title", function(e){
        var index = $(this).index();
        if (!$filterItem.eq(index).hasClass("active")) {
            $(this).children("span").children("i").removeClass("fa-angle-down").addClass("fa-angle-up");
            $(this).siblings(".filter-title").children("span").children("i").removeClass("fa-angle-up").addClass("fa-angle-down");
            $filterItem.eq(index).addClass("active").siblings(".filter-item").removeClass("active");
            $(".display-mask").show();
        } else {
            $(this).children("span").children("i").removeClass("fa-angle-up").addClass("fa-angle-down");
            $filterItem.eq(index).removeClass('active');
            $(".display-mask").hide();
            updateFilterDateDisplay();
        }
    });
    $(".display-mask").on("click", function(e) {
        $(this).hide();
        $filterItem.removeClass('active');
        updateFilterDateDisplay();
        cur_page = 1;
        next_page = 1;
        total_page = 1;
        updateHouseData("renew");

    });
    $(".filter-item-bar>.filter-area").on("click", "li", function(e) {
        if (!$(this).hasClass("active")) {
            $(this).addClass("active");
            $(this).siblings("li").removeClass("active");
            $(".filter-title-bar>.filter-title").eq(1).children("span").eq(0).html($(this).html());
        } else {
            $(this).removeClass("active");
            $(".filter-title-bar>.filter-title").eq(1).children("span").eq(0).html("位置区域");
        }
    });
	
	
	
	
	
	
	
	
		
	laydate({
		elem: '#hello', 
		event: 'focus' 
	});

	var start = {
		elem: '#start',
		format: 'YYYY/MM/DD hh:mm:ss',
		min: laydate.now(), 
		max: '2099-06-16 23:59:59', 
		istime: true,
		istoday: false,
		choose: function (datas) {
			end.min = datas; 
			end.start = datas 
		}
	};
	var end = {
		elem: '#end',
		format: 'YYYY/MM/DD hh:mm:ss',
		min: laydate.now(),
		max: '2099-06-16 23:59:59',
		istime: true,
		istoday: false,
		choose: function (datas) {
			start.max = datas; 
		}
	};
	laydate(start);
	laydate(end);

})