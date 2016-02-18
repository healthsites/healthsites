/**
 * Created by meomancer on 18/02/16.
 */
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
    if (v_width <= 991) {
        var pad = r_height / 2;
        $('.location-info').css('margin-top', h_height + pad);
        $('.map-page#map').css('top', h_height);
        $('#map, #map-home').css('height', pad);
        $('#map, #map-home').css('width', v_width);

        //mobile country search
        $('.select-country input').focusin(function () {
            $('body').addClass('search-focus');
        });
        $('.select-country input').focusout(function () {
            $('body').removeClass('search-focus');
        });

    }
    else {
        if ($('.select-country').length > 0) {
            var c_height = $('.country-data').css('height');
        }
        $('.location-info').css('margin-top', h_height);
        $('.map-page #map').css('height', v_height - h_height);
        $('.map-page #map').css('width', v_width - s_width);
        $('.map-page #map').css('top', h_height);
        $('body').removeClass('search-focus');
        $('#map, #map-home').css('height', c_height);
    }
}