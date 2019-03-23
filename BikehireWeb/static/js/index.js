
$(function () {
    $(window).on("resize", function () {
        // 1.1 Get the width of the window
        let clientW = $(window).width();
        // console.log(clientW);

        // 1.2 Set threshold
        let isShowBigImage = clientW >= 800;

        // 1.3 Get all the items
        let $allItems = $("#lk_carousel .item");
        // console.log($allItems);

        // 1.4 Traversing
        $allItems.each(function (index, item) {
            // 1.4.1 Take the path of the picture
            let src = isShowBigImage ? $(item).data("lg-img") : $(item).data("sm-img");
            let imgUrl = 'url("' + src +'")';

            // 1.4.2 Set background
            $(item).css({
                backgroundImage: imgUrl
            });

            // 1.4.3 Set img tag
            if(!isShowBigImage){
                let $img = "<img src='" + src + "'>";
                $(item).empty().append($img);
            }else {
                $(item).empty();
            }

        });
    });

    $(window).trigger("resize");



    // 2. tooltip
    $('[data-toggle="tooltip"]').tooltip();

    // 3. Dynamic processing width
    $(window).on("resize", function () {
        let $ul = $("#lk_product .nav");
        let $allLis = $("[role='presentation']", $ul);
        // console.log($allLis);

        // 3.1 Traversing
        let totalW = 0;
        $allLis.each(function (index, item) {
            totalW += $(item).width();
        });

        // console.log(totalW);

        let parentW = $ul.parent().width();

        // 3.2 Set width
        if(totalW > parentW){
            $ul.css({
                width: totalW + "px"
            })
        }else {
            $ul.removeAttr("style");
        }
    });


    // 4. Navigation processing
    let allLis = $("#lk_nav li");

    $(allLis[2]).on("click", function () {
        $("html,body").animate({ scrollTop: $("#lk_hot").offset().top }, 1000);
    });


    $(window).trigger("resize");
});