$(document).ready(function () {
    // set share url
    var baseURL = location.protocol + "//" + location.hostname + "/";
    if ($(".twitter-href").length !== 0) {
        $(".twitter-href").attr("href", "https://twitter.com/intent/tweet?text=Share and develop healthsite data on " + baseURL);
    }
    if ($(".facebook-href").length !== 0) {
        $(".facebook-href").attr("href", "https://www.facebook.com/sharer/sharer.php?u=" + baseURL);
    }
    if ($(".googleplus-href").length !== 0) {
        $(".googleplus-href").attr("href", "https://plus.google.com/share?url=" + baseURL);
    }

    if ($("#slider").length !== 0) {
        $('#slider').slick({
            dots: true,
            infinite: false,
            speed: 300,
            slidesToShow: 1,
            adaptiveHeight: true,
            fade: true,
            centerMode: true,
        });
    }

    // TODO: Please fix this
    // $('#navbar a').click(function () {
        // var match = jQuery(this).attr('href').match(/#\S+/);
        // if (match) {
        //     console.log(match);
        //     ga('send', 'pageview', location.pathname + match[0]);
        // }
    // });
})