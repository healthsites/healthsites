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
        $('.map-page #map').css('top', h_height);
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

    // set top of report popup
    var offset = $('#map').offset();
    if (offset) {
        $('#report-popup').css('top', $('#map').css('top'));
        $('#report-popup').css('left', ($('#map').width() / 2) + offset.left);
    }
}

function policyshow() {
    $('body').prepend('<div id="policy" class="fixed"><p>healthsites.io cannot guarantee the validity of the information found here <a href="https://github.com/healthsites/healthsites/wiki/Healthsites---terms-of-use" target="_blank">Terms of use</a> <a href="#" class="accept">Accept</a></p></div>');
    $('body').addClass('policy-enabled');
    $('.accept').click(function () {
        $('#policy').slideUp(300);
        $('body').removeClass('policy-enabled');
    });
    return false;
}

function renderCredit() {
    /* map credits */
    $("#map").append("<a class='credits' href='#'>&copy;</a>");
    $(".credits").click(function () {
        $(this).hide();
        $(".leaflet-bottom.leaflet-right").show();
        $(".leaflet-bottom.leaflet-right").prepend("<a class='close' href='#'>x</a>");
        return false;
    });
    $(".leaflet-bottom").delegate('.close', 'click', function () {
        $(this).hide();
        $(".leaflet-bottom.leaflet-right").hide();
        $(".credits").show();
        return false;
    });
}

function changePage(element) {
    var childs = $("#updates-wrapper").children();
    var activeChild = $("#updates-wrapper").children(".graph.updates:visible");
    var activeindex = $(activeChild).attr('id').split("-")[1];
    var newActiveIndex = parseInt(activeindex);
    if ($(element).hasClass("prev")) {
        if (activeindex > 0) {
            newActiveIndex -= 1;
        }
    } else if ($(element).hasClass("next")) {
        if (activeindex + 1 < childs.length) {
            newActiveIndex += 1;
        }
    }
    $(activeChild).hide();
    $("#updates-" + newActiveIndex).show();
    updateButton();
    return false;
}

function updateButton() {
    var childs = $("#updates-wrapper").children();
    var activeChild = $("#updates-wrapper").children(".graph.updates:visible");
    var activeindex = $(activeChild).attr('id').split("-")[1];
    $(".prev").removeClass("opacity-7");
    $(".next").removeClass("opacity-7");
    if (activeindex == 0) {
        $(".prev").addClass("opacity-7");
    }
    if (activeindex + 1 >= childs.length) {
        $(".next").addClass("opacity-7");
    }
}