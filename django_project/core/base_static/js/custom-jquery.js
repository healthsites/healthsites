$(document).ready(function(){	
    
	//activate searchbar
	$('.navbar-search').click(function() {
      $("body").toggleClass("searchbar-active");
	  $(".navbar-search i").toggleClass("fa-search fa-times");
	  return false;
    });
	
	//activate social login/share
	$('.navbar-share').click(function() {
      $("#site-social").toggleClass("hidden");
	  $(".navbar-share").toggleClass("closed");
	   return false;
    });
	
	$('.nav a').on('click', function(){
    $('.btn-navbar').click(); //bootstrap 2.x
    $('.navbar-toggle').click() //bootstrap 3.x by Richard
});
	
	$('.js-fullheight').css('height', $(window).height());
	
	
	$('a[href*=#]:not([href=#])').click(function() {
    if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
      if (target.length) {
        $('html,body').animate({
          scrollTop: target.offset().top
        }, 1000);
        return false;
      }
    }
  });
	
 
  
  if (v_width<=991) {
	  var pad = v_height/2;
	  $('.location-info').css('margin-top',pad);
	  $('#map, #map-home').css('height',pad);
	  $('#map, #map-home').css('width',v_width);
	   var h_height = $('.masthead').height();
  var v_height = $(window).height();
  var v_width = $(window).width();
  var s_width = $('.location-info').width();
  $('#map').css('height', v_height - h_height);
  $('#map').css('width', v_width - s_width);
  }
	else {
		 $('.location-info').css('margin-top',0);

	}
	var v_count = '0';
	
	$('#slider').rhinoslider({
					effect: 'fade',
					controlsMousewheel: false,
					controlsPrevNext: true,
					controlsPlayPause: true,
					autoPlay: false,
					showBullets: 'always',
					showControls: 'always'
				});
	
	$('.timer').each(function(){
			var imagePos = $(this).offset().top;			
			var topOfWindow = $(window).scrollTop();
			if (imagePos < topOfWindow+500 && v_count=='0') {		
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
		
if (v_width<=991) {
	var getslidewd= $('.main-img').width();
	var getslidehi= getslidewd*0.85;
	$('.rhino-container').width(getslidewd);
	$('.rhino-container').height(getslidehi);
	$('.rhino-container #slider li').width(getslidewd);
	$('.rhino-container #slider li').height(getslidehi);
	}
});
	
//hide/show tagline on scroll
$(window).scroll(function() {    
  var scroll = $(window).scrollTop();
  if (scroll >= 72) {
	  $("#navbar-wrapper").addClass("no-tag");
  } else {
	  $("#navbar-wrapper").removeClass("no-tag");
  }
});



$(window).resize(function() {
  var h_height = $('.masthead').height();
  var v_height = $(window).height();
  var v_width = $(window).width();
  var s_width = $('.location-info').width();
  $('.js-fullheight').css('height', $(window).height());
  $('#map').css('height', v_height - h_height);
  $('#map').css('width', v_width - s_width);
  if (v_width<=991) {
	  var pad = v_height/2;
	  $('.location-info').css('margin-top',pad);
	  $('#map, #map-home').css('height',pad);
	  $('#map, #map-home').css('width',v_width);
	  var getslidewd= $('.main-img').width();
var getslidehi= getslidewd*0.85;
$('.rhino-container').width(getslidewd);
$('.rhino-container').height(getslidehi);
$('.rhino-container #slider li').width(getslidewd);
$('.rhino-container #slider li').height(getslidehi);
  }
  else {
	   $('.location-info').css('margin-top',0);
	   $('#map-home').css('width','50%');
	   $('#map-home').css('height', 645);
	   $('.rhino-container').width("100%");
$('.rhino-container').height(688);
$('.rhino-container #slider li').width("100%");
$('.rhino-container #slider li').height(688);
  }
});
