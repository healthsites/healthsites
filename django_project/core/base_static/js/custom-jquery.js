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
		   window.history.pushState("", "", '#'+this.hash.slice(1));
        return false;
      }
    }
  });
	
   
  $("#locality-name").bind("DOMSubtreeModified",function(){
      $(this).parent().stop().animate({ backgroundColor: "#f44a52",
	                                    color: "#fff" }, 100)
	                         .animate({ backgroundColor: "white",
							            color: "#3c4c57" }, 550);
  });
  
  var v_width = $(window).width();
  var v_height = $(window).height();
  var h_height = $('.masthead').height();
  var s_width = $('.location-info').width();
  
  if (v_width<=991) {
	  
      
     
	  var pad = v_height/2;
	  $('.location-info').css('margin-top',pad);
	  $('.map-page #map, #map-home').css('height',pad);
	  $('.map-page #map, #map-home').css('width',v_width);
	   
  
 
  }
	else {
		 $('.location-info').css('margin-top',0);
         $('.map-page #map').css('height', v_height - h_height);
         $('.map-page #map').css('width', v_width - s_width);
	}
	
	var v_count = '0';
	
	
	
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
		

});
	
//hide/show tagline on scroll
$(window).scroll(function() {    
  var scroll = $(window).scrollTop();
  if (scroll >= 72) {
	  $(".home .masthead").addClass("no-tag");
  } else {
	  $(".home .masthead").removeClass("no-tag");
  }	
  

  
});



$(window).resize(function() {
  var h_height = $('.masthead').height();
  var v_height = $(window).height();
  var v_width = $(window).width();
  var s_width = $('.location-info').width();
  $('.js-fullheight').css('height', $(window).height());
  $('.map-page #map').css('height', v_height - h_height);
  $('.map-page #map').css('width', v_width - s_width);
  if (v_width<=991) {
	  var pad = v_height/2;
	  $('.location-info').css('margin-top',pad);
	  $('.map-page #map, #map-home').css('height',pad);
	  $('.map-page #map, #map-home').css('width',v_width);
	  var getslidewd= $('.main-img').width();
  }
  else {
	   $('.location-info').css('margin-top',0);
	   $('#map-home').css('width','50%');
	   $('#map-home').css('height', 621);
  }
});

