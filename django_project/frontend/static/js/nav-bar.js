var search_localities_name_url = "/search/localities/name";
var search_geoname_url = "http://gd.geobytes.com/AutoCompleteCity";
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

    function set_search_url(url, data_type) {
        $("#search-box").autocomplete({
            source: function (request, response) {
                $.ajax({
                    url: url,
                    dataType: data_type,
                    data: {
                        q: request.term
                    },
                    success: function (data) {
                        response(data);
                    }
                });
            },
            minLength: 3,
            select: function (event, ui) {

            },
            open: function () {
                $(this).removeClass("ui-corner-all").addClass("ui-corner-top");
            },
            close: function () {
                $(this).removeClass("ui-corner-top").addClass("ui-corner-all");
            }
        });
    }

    set_search_url(search_localities_name_url);
    $('input:radio[name=option]').change(function () {
        // set text default for search box
        $("#search-box").val("");

        // set data for autocomplete
        if (this.value == 'place') {
            set_search_url(search_geoname_url, 'jsonp');
        } else if (this.value == 'healthsite') {
            set_search_url(search_localities_name_url, 'json');
        } else {
            set_search_url(search_localities_name_url, 'json');
        }
    });
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
})