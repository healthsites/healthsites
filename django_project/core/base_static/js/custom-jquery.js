$(document).ready(function(){	
    
	//activate searchbar
	$('.navbar-search').click(function() {
      $("body").toggleClass("searchbar-active");
	  $(".navbar-search i").toggleClass("fa-search fa-times");
    });
	
	//activate social login/share
	$('.navbar-share').click(function() {
      $("#site-social").toggleClass("hidden");
	  $(".navbar-share i").toggleClass("fa-share-alt fa-times");
    });
	
	//hide/show tagline on scroll
	$(window).scroll(function() {    
	  var scroll = $(window).scrollTop();
	  if (scroll >= 72) {
		  $(".masthead").addClass("no-tag");
	  } else {
		  $(".masthead").removeClass("no-tag");
	  }	
	});
	
	$('.js-fullheight').css('height', $(window).height());


});