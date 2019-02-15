/**
 * Created by meomancer on 21/03/16.
 */
//{# FOR UPDATING CHART #}
function updateChart(hospital, medical, orthopedic) {
    var hospital_per = hospital / (hospital + medical + orthopedic);
    var medical_per = medical / (hospital + medical + orthopedic);
    var orthopedic_per = orthopedic / (hospital + medical + orthopedic);
    chart.load({
        columns: [
            //the healthsites names
            ['x', 'Hospitals', 'Medical clinic', 'Orthopaedic clinic'],
            //the healthsites number
            ['number', hospital, medical, orthopedic],
            //the healthsites percentgage
            ['percent', hospital_per, medical_per, orthopedic_per]
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
    var country = $("#country-form").find("#country-search-box")[0].value;
    event.preventDefault();
    gettingData(country);
});


function gettingData(country) {
    // Get count of country
    $("#country-locality-number").html(0);
    $.ajax({
        url: "/api/v2/facilities/count",
        dataType: 'json',
        data: {
            country: country
        },
        success: function (data) {
            $("#country-locality-number").html(data);
            if (country === 'World') {
                $('#healthsites-count').html('<span class="timer" data-speed="2500"  data-to="' + data + '">' + data + '</span>');
            }
        }
    });

    $.ajax({
        url: "/search/localities/country",
        dataType: 'json',
        data: {
            q: country
        },
        success: function (data) {
            $APP.trigger('map.update-geoname', {'geoname': country});
            $("#updates-wrapper").html('<div id="updates-1" class="graph updates"><div class="entry">-</div></div>');
            updateChart(0, 0, 0);

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
            if (data.numbers) {
                updateChart(data.numbers.hospital, data.numbers.medical_clinic, data.numbers.orthopaedic_clinic);
            }
            if (data.completeness) {
                updatePieChart(data.completeness.basic, data.completeness.partial, data.completeness.complete);
            }
            if (data.last_update.length > 0) {
                $("#updates-wrapper").html("");
                for (var i = 0; i < data.last_update.length; i++) {
                    var page = parseInt(i / 5);
                    var wrapper = $("#updates-" + page);
                    if (wrapper.length > 0) {

                    } else {
                        $("#updates-wrapper").append('<div id="updates-' + page + '" class="graph updates"></div>');
                        wrapper = $("#updates-" + page);
                        if (page != 0) {
                            wrapper.hide();
                        }
                    }
                    var update = data.last_update[i];
                    var html = "<div class=\"entry\">";
                    html += "<div class=\"entry\">";
                    html += "<span class=\"date\">" + getDateString(update.date_applied) + "</span> - ";
                    html += "<span class=\"name\">";
                    html += "<a href=\"profile/" + update.author + "\">@" + update.author_nickname + "</a></span> - ";
                    var mode = "";
                    if (update.mode == 1) {
                        mode = "added";
                    } else {
                        mode = "amended";
                    }
                    //{# update the html #}
                    if (update.data_count == 1) {
                        html += "<a href=\"map#!/locality/" + update.locality_uuid + "\" class=\"location-name\">" + data.last_update[i].locality + "</a>";
                        html += "<span class=\"location-name\"> " + mode + " </span>";
                    } else {
                        html += "<span class=\"location-name\">" + data.last_update[i].data_count + " HS/" + mode + "</span>";
                    }
                    html += "</div>";
                    wrapper.append(html);
                }
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