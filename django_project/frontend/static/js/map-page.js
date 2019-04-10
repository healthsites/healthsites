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

function onChange(element) {
    $APP.trigger('sidebar.option-onchange', {'element': element});
}
function onKeyPress(element) {
    if (element.id == "locality-phone-input-int") {
        var val = $(element).val();
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
function prerender_popup() {
    var $popup = $("#report-popup");
    $popup.css("margin-top", ($popup.height() + 20) * -1)
    $("#report-button").click(function () {
        var uuid = $("#report-popup-text").val();
        if (uuid.length > 0) {
            if (uuid != null) {
                $APP.trigger('sidebar.report-duplication', {'uuid': uuid});
            }
            toogle_popup();
        }
    });
    $("#cancel-report-button").click(function () {
        toogle_popup();
    });
}
function hide_popup() {
    if ($("#report-popup").is(":visible")) {
        toogle_popup();
    }
}
function toogle_popup() {
    var $popup = $("#report-popup");
    var marginTop = 20;
    var height = $popup.height();
    if ($popup.is(":visible")) {
        $popup.animate({
            opacity: 0.0,
            marginTop: (height + marginTop) * -1,
        }, 200, function () {
            // Animation complete.
            $popup.hide();
        });
    } else {
        $("#report-popup-text").val("");
        $popup.show();
        $popup.animate({
            opacity: 1.0,
            marginTop: marginTop,
        }, 200, function () {
        });
    }
}

function synonyms_clicked(element) {
    var uuid = $(element).attr('id');
    $APP.trigger('locality.map.click', {'locality_uuid': uuid});
    $APP.trigger('set.hash.silent', {'locality': uuid});
}