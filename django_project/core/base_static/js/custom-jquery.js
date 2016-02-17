function mapcount() {
 var v_width = $(window).width();
 var v_height = $(window).height();
 var s_height = $('.nav-searchbar').height();
 if ($('.nav-searchbar').is(":visible")) {
 var h_height = $('.masthead').height() + s_height;
 }
 else {
	 var h_height = $('.masthead').height();
 }
 var s_width = $('.location-info').width();
 var r_height = v_height - h_height;



  if (v_width<=991) {



	  var pad = r_height/2;
	  $('.location-info').css('margin-top',h_height + pad);
	  $('#map').css('top', h_height);
	  $('#map, #map-home').css('height',pad);
	  $('#map, #map-home').css('width',v_width);

        //mobile country search
		$('.select-country input').focusin(function() {
			$('body').addClass('search-focus');
		});
		$('.select-country input').focusout(function() {
			$('body').removeClass('search-focus');
		});

  }
	else {
		 if ($('.select-country').length>0) {
            var s_height = $('.select-country').height();
         }
		 $('.location-info').css('margin-top',h_height);
         $('.map-page #map').css('height', v_height - h_height);
         $('.map-page #map').css('width', v_width - s_width);
		 $('.map-page #map').css('top', h_height);
		 $('body').removeClass('search-focus');
		 $('#map-home').css('height', s_height);
	     $('#map-home').css('width', s_height);
	}
}


$(document).ready(function () {

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
        $('.btn-navbar').click(); //bootstrap 2.x
        $('.navbar-toggle').click() //bootstrap 3.x by Richard
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
        if ( $(this).hasClass("search" ) && $(this).hasClass("active" )) {
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
    } else {
        $(".home .masthead").removeClass("no-tag");
    }


});

$(window).resize(function () {
    mapcount();
});
