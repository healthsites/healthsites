/**
 * Created by meomancer on 21/03/16.
 */
//{# FOR UPDATING CHART #}
function updateChart(number_of_data, data) {
    var xValue = ['x'];
    var numberValue = ['number'];
    var percentValue = ['percent'];
    $.each(data, function (key, value) {
        xValue.push(key);
        numberValue.push(value);
        percentValue.push(value / number_of_data);
    });
    chart.load({
        columns: [
            //the healthsites names
            xValue,
            //the healthsites number
            numberValue,
            //the healthsites percentgage
            percentValue
        ]
    });
}

function updatePieChart(basic, partial, complete) {
    piechart.load({
        columns: [
            ['complete', complete],
            ['partial', partial],
            ['basic', basic],
        ],
    });
}


$("#country-form").submit(function (event) {
    var $input = $($(this).find("#country-search-box")[0]);
    var $searchIcon = $(this).find('.fa-search');
    var country = $input.val();
    event.preventDefault();
    $input.prop("disabled", true);
    $searchIcon.removeClass('fa-search');
    $searchIcon.addClass('fa-circle-o-notch');
    $searchIcon.addClass('fa-spin');
    gettingData(country, function () {
        $input.prop("disabled", false);
        $searchIcon.addClass('fa-search');
        $searchIcon.removeClass('fa-circle-o-notch');
        $searchIcon.removeClass('fa-spin');
    });

});


function gettingData(country, callback) {
    // Get count of country
    $("#country-locality-number").html(0);
    $.ajax({
        url: "/api/v2/facilities/statistic",
        dataType: 'json',
        data: {
            country: country
        },
        success: function (data) {
            if (callback) {
                callback();
            }
            $APP.trigger('map.update-geoname', {'geoname': country});
            //{# default #}
            $("#country-locality-number").html(0);
            $("#updates-wrapper").html('<div id="updates-1" class="graph updates"><div class="entry">-</div></div>');

            //{# show the real data #}
            //{# country title #}
            if (country == "") {
                country = "World";
                $("#country-title").attr('href', "#");
            } else {
                $("#country-title").attr('href', "map?country=" + country);
            }
            $("#country-title").html(country);

            // creating polygon
            var polygon_raw = data.polygon;
            if (polygon_raw) {
                var polygon_json = JSON.parse(polygon_raw);
                var polygon = polygon_json['coordinates'];
                $APP.trigger('map.create-polygon', {'polygon': polygon});
            }

            //{# country healthsite number #}
            if (data.localities) {
                $("#country-locality-number").html(data.localities);
                if (data.numbers) {
                    updateChart(data.localities, data.numbers);
                }
            }
            if (data.completeness) {
                updatePieChart(data.completeness.basic, data.completeness.partial, data.completeness.complete);
            }
            if (data.last_update.length > 0) {
                $("#updates-wrapper").html("");
                $.each(data.last_update, function (i, update) {
                    var page = parseInt(i / 5);
                    var wrapper = $("#updates-" + page);
                    if (wrapper.length == 0) {
                        $("#updates-wrapper").append('<div id="updates-' + page + '" class="graph updates"></div>');
                        wrapper = $("#updates-" + page);
                        if (page != 0) {
                            wrapper.hide();
                        }
                    }
                    var html = "<div class=\"entry\">";
                    html += "<div class=\"entry\">";
                    html += "<span class=\"date\">" + getDateString(update.changeset_timestamp) + "</span> - ";
                    html += "<span class=\"name\">";
                    html += "<a href=\"profile/" + update.changeset_user + "\">@" + update.changeset_user + "</a></span> - ";
                    var mode = "";
                    if (update.changeset_version == 1) {
                        mode = "added";
                    } else {
                        mode = "amended";
                    }
                    //{# update the html #}
                    html += "<a href=\"map#!/locality/" + update.locality_uuid + "\" class=\"location-name\">" + update.name + "</a>";
                    html += "<span class=\"location-name\"> " + mode + " </span>";
                    html += "</div>";
                    wrapper.append(html);
                });
                updateButton();
            }

            //{# set view port #}
            if (data.viewport) {
                var northeast_lat = parseFloat(data.viewport.northeast_lat);
                var northeast_lng = parseFloat(data.viewport.northeast_lng);
                var southwest_lat = parseFloat(data.viewport.southwest_lat);
                var southwest_lng = parseFloat(data.viewport.southwest_lng);
                if (southwest_lat != 0.0 && southwest_lng != 0.0 && northeast_lat != 0.0 && northeast_lng) {
                    map._setFitBound(southwest_lat, southwest_lng, northeast_lat, northeast_lng);
                    $APP.trigger('map.update-bound', {
                        'southwest_lat': southwest_lat,
                        'southwest_lng': southwest_lng,
                        'northeast_lat': northeast_lat,
                        'northeast_lng': northeast_lng
                    });
                }
            }
            mapcount();
            $APP.trigger('map.rerender');
        }
    });
}