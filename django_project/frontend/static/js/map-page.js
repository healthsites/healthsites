/**
 * Created by meomancer on 21/03/16.
 */
var $country_table;
var countries = [];
var titleRow = ["A - E", "F - J", "K - O", "P - T", "U - Z"];
var titleRowRegex = [/[a-e]/, /[f-j]/, /[k-o]/, /[p-t]/, /[u-z]/];

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(returnPosition);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}
function returnPosition(position) {
    $APP.trigger('map.pan', {'location': [position.coords.latitude, position.coords.longitude]});
}

function loadCountry(country) {
    var country_id = country.split(".").join("-");
    country_id = country_id.split("&#39;").join("-");
    country_id = country_id.split(" ").join("-");
    country_id = country_id.split("(").join("-");
    country_id = country_id.split(")").join("-");
    var html = '<div class="block-data"><span class="col-xs-6"><a href="map?country=' + country + '">' + country + '</a></span> <span id="' + country_id + '-number" class="col-xs-3">loading</span> <span id="' + country_id + '-complete" class="col-xs-3">loading</span></div>';
    $.ajax({
        number: country_id + "-number",
        completeness: country_id + "-complete",
        url: "/search/localities/country",
        dataType: 'json',
        data: {
            q: country
        },
        success: function (data) {
            var number = 0;
            var completness = 0;
            if (data.localities > 0) {
                completness = data.completeness.complete / data.localities * 100;
                number = data.localities;
            }
            $("#" + this.number).html(number);
            $("#" + this.completeness).html(completness);
        },
        fail: function (data) {
            $("#" + this.number).html("fail");
            $("#" + this.completeness).html("fail");
        }
    });
    return html;
}
function loadByAlphabet(index) {
    var wrapper = $("#title-row-" + index);
    if (wrapper.html() == "") {
        var found = false;
        for (var i = 0; i < countries.length; i++) {
            if (countries[i].toLowerCase()[0].match(titleRowRegex[index]) != null) {
                found = true;
                wrapper.append(loadCountry(countries[i]));
            } else {
                if (found) break;
            }
        }
        wrapper.css("height", "auto");
    }
}

function onChange(element) {
    $APP.trigger('sidebar.option-onchange', {'element': element});
}
function onKeyPress(element) {
    if (element.id == "locality-phone-input-int") {
        var val = $(element).val();
        console.log(val);
        if (val.length > 3) {
            val = val.substring(0, 3);
            $(element).val(val);
        }
    }
}
function addOption(element) {
    $APP.trigger('sidebar.option-add', {'element': element});
}
function addOthers() {
    $APP.trigger('sidebar.other-add');
}
function changeTag(value) {
    $APP.trigger('sidebar.tag-onchange', {'value': value});
}

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
$('body').on("click", ".remove_option", function (e) { //user click on remove text
    e.preventDefault();
    $(this).parent('div').remove();
})
$('body').on("click", ".remove_tag", function (e) { //user click on remove text
    e.preventDefault();
    $(this).parent('li').remove();
})
$("#see-more-list").click(function () {
    var lastChilds = $('#full-list').children();
    var date = "";
    if (lastChilds.length == 0) {
        if (typeof $("#last_update").data("data") !== "undefined") {
            date = $("#last_update").data("data").date;
        }
    } else {
        date = $(lastChilds.last()).data("data").date;
    }
    var uuid = $(this).data("data").uuid;
    $.ajax({
        url: "/locality/updates",
        dataType: 'json',
        data: {
            date: date,
            uuid: uuid,
        },
        success: function (data) {
            if (data.length < 10) {
                $("#see-more-list").hide();
            }
            for (var i = 0; i < data.length; i++) {
                var html = '<div>';
                html += '<span class="date">' + getDateString(data[i]['last_update']) + '</span>, by';
                html += '<span class="name">';
                html += ' <a href="profile/' + data[i]['uploader'] + '">@' + data[i]['nickname'] + '</a>';
                html += '</span>';
                html += '<span>';
                html += ' - <a style="cursor:pointer" onclick="gotochangeset(\'' + data[i]['changeset_id'] + '\',\'' + uuid + '\')">' + data[i]['changeset_id'] + '</a>';
                html += '</span>';
                html += '</div>';
                $('#full-list').append(html);
                var lastChilds = $('#full-list').children();
                $(lastChilds.last()).data("data", {date: data[i]['last_update']});
            }
        },
    });
})
$("#geolocate").click(function () {
    getLocation();
})
function gotochangeset(changeset, uuid) {
    window.location.href = "/map#!/locality/" + uuid + "/" + changeset;
}
function split(element) {
    $(element).html('and');
    $(element).parent('tr').find('.time2').css({'opacity': 1});
    $(element).parent('tr').find('.unsplit').css({'opacity': 1});
    $(element).parent('tr').find('.unsplit').css({'cursor': 'pointer'});
    // change disable/enabled
    $(element).parent('tr').find('.time2').find('input').prop('disabled', false);
    $APP.trigger('sidebar.split-event');

}
function shortcutDefiningHour(shortcut) {
    var days = 0;
    if (shortcut == "24/7") {
        days = 7;
    } else {
        days = 5;
    }
    var daysCheckbox = $("#locality-operating-hours-input-table").find('.daycheckbox');
    for (var i = 0; i < daysCheckbox.length; i++) {
        if (i < days) {
            $(daysCheckbox[i]).prop("checked", true);
        } else {
            $(daysCheckbox[i]).prop("checked", false);
        }
    }
    var unsplits = $("#locality-operating-hours-input-table").find('.unsplit');
    for (var i = 0; i < unsplits.length; i++) {
        if ($(unsplits[i]).css('opacity') == 1.0) {
            unsplit(unsplits[i]);
        }
        var input1 = $(unsplits[i]).parent('tr').find('.time1').find('input');
        var input2 = $(unsplits[i]).parent('tr').find('.time2').find('input');
        if (input1.length == 2) {
            $(input1[0]).val('00:00');
            $(input1[1]).val('23:59');
        }
        if (input2.length == 2) {
            $(input2[0]).val('00:00');
            $(input2[1]).val('23:59');
        }
    }
    $APP.trigger('sidebar.split-event');
}
function unsplit(element) {
    $(element).css({'opacity': 0.0});
    $(element).parent('tr').find('.time2').css({'opacity': 0.0});
    $(element).parent('tr').find('.split').html('<a>split</a>');
    $(element).parent('tr').find('.unsplit').css({'cursor': 'default'});
    $(element).parent('tr').find('.time2').find('input').val('00:00');
    // change disable/enabled
    $(element).parent('tr').find('.time2').find('input').prop('disabled', true);
    $APP.trigger('sidebar.split-event');

}