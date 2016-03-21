$(document).ready(function () {
    var v_width = $(window).width();
    //activate cookiebar
    $.cookieBar({
        declineButton: true,
        fixed: true
    });

    //activate searchbar
    $('.navbar-search, #icons-nav .search').click(function () {
        $("body").toggleClass("searchbar-active");
        $(".navbar-search i").toggleClass("fa-search fa-times");
        mapcount();
        return false;
    });

    //activate social login/share
    $('.navbar-share').click(function () {
        $("#site-social").toggleClass("hidden");
        $(".navbar-share").toggleClass("closed");
        return false;
    });

    $('.nav a').not('.navbar-search').on('click', function () {
        if (v_width <= 767) {
            $('.btn-navbar').click(); //bootstrap 2.x
            $('.navbar-toggle').click() //bootstrap 3.x by Richard
        }
    });

    $('.js-fullheight').css('height', $(window).height());


    $('a[href*=#]:not([href=#])').click(function () {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                $('html,body').animate({
                    scrollTop: target.offset().top
                }, 1000);
                window.history.pushState("", "", '#' + this.hash.slice(1));
                return false;
            }
        }
    });

    $('#icons-nav a').click(function () {
        $(this).toggleClass("active");
        $(this).siblings().removeClass("active");
        if ($(this).hasClass("search") && $(this).hasClass("active")) {
            $(".search-block").show();
        }
        else {
            $(".search-block").hide();
        }
    });

    $("#locality-name").bind("DOMSubtreeModified", function () {
        $(this).parent().stop().animate({
                backgroundColor: "#f44a52",
                color: "#fff"
            }, 100)
            .animate({
                backgroundColor: "white",
                color: "#3c4c57"
            }, 550);
    });

    mapcount();

    /* timer */
    var v_count = '0';


    $('.timer').each(function () {
        var imagePos = $(this).offset().top;
        var topOfWindow = $(window).scrollTop();
        if (imagePos < topOfWindow + 500 && v_count == '0') {
            $(function ($) {
                // start all the timers
                $('.timer').each(count);
                function count(options) {
                    v_count = '1';
                    var $this = $(this);
                    options = $.extend({}, options || {}, $this.data('countToOptions') || {});
                    $this.countTo(options);
                }
            });
        }
    });


});

//hide/show tagline on scroll
$(window).scroll(function () {
    var scroll = $(window).scrollTop();
    if (scroll >= 72) {
        $(".home .masthead").addClass("no-tag");
		$(".home").addClass("h-short");
    } else {
        $(".home .masthead").removeClass("no-tag");
		$(".home").removeClass("h-short");
    }


});

$(window).resize(function () {
    mapcount();
});
