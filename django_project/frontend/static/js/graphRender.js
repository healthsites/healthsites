/**
 * Created by meomancer on 04/12/15.
 */

var chart = c3.generate({
    bindto: '#chart1',
    size: {
        height: 220
    },
    bar: {
        width: 18
    },
    data: {
        x: 'x',
        y: 'percent',
        columns: [
            //the healthsites names
            ['x', 'Hospitals', 'Medical clinic', 'Orthopaedic clinic'],
            //the healthsites number
            ['number', 0, 0, 0],
            //the healthsites percentgage
            ['percent', 0, 0, 0]
        ],
        axes: {
            number: 'y2'
        },
        types: {
            percent: 'bar',
            number: 'bar'
        },
        order: 'asc',

        labels: {
            format: {
                number: function (v, id, i, j) {
                    return v;
                },
            }
        },


    },
    axis: {
        rotated: true,
        x: {
            type: 'category',

        },
        y: {
            max: 1,
            tick: {
                values: [0, 0.5, 1],
                format: d3.format('%,')

            }
        }
    },
    legend: {
        show: false
    },
    color: {
        pattern: ['#b6cccc', '#f89ea1']
    }
});

var piechart = c3.generate({
    bindto: '#piechart',
    size: {
        height: 220
    },
    data: {
        // iris data from R
        columns: [
            ['complete', 0],
            ['partial', 0],
            ['basic', 0],
        ],
        colors: {
            complete: '#f89ea1',
            partial: '#b6cccc',
            basic: '#8698a4'
        },
        type: 'pie',
        onclick: function (d, i) {
            console.log("onclick", d, i);
        },
        onmouseover: function (d, i) {
            console.log("onmouseover", d, i);
        },
        onmouseout: function (d, i) {
            console.log("onmouseout", d, i);
        }
    }
});

$(document).ready(function () {
    $("#country-search-box").autocomplete({
        source: function (request, response) {
            $.ajax({
                url: "{% url 'countries' %}",
                dataType: 'json',
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

    //{# FOR
    //    UPDATING
    //    CHART #
    //}
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

    //# first init #
    gettingData("");

    function gettingData(country) {
        $.ajax({
            url: "{% url 'locality-country-search' %}",
            dataType: 'json',
            data: {
                q: country
            },
            success: function (data) {
                //{# default #}
                $("#country-locality-number").html(0);
                updateChart(0, 0, 0);

                //{# show the real data #}
                //{# country title #}
                if (country == "") country = "World";
                $("#country-title").html(country);

                //{# country healthsite number #}
                if (data.localities) {
                    $("#country-locality-number").html(data.localities);
                }
                if (data.numbers) {
                    updateChart(data.numbers.hospital, data.numbers.medical_clinic, data.numbers.orthopaedic_clinic);
                }
                if (data.completeness) {
                    updatePieChart(data.completeness.basic, data.completeness.partial, data.completeness.complete);
                }
                console.log(data);
            }
        });
    }

    // initialize the app
    //{#            new APP();#}
    // We need different app for the home page. Adapt from the current app.
});