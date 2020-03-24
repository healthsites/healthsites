require.config({
    baseUrl: '/static/',
    paths: {
        'jquery': 'libs/jquery.js/3.3.1/jquery.min',
        'jquery-ui': 'libs/jquery.js/1.12.1/jquery-ui.min',
        'backbone': 'libs/backbone.js/1.4.0/backbone-min',
        'underscore': 'libs/underscore.js/1.9.1/underscore-min',
        'bootstrap': 'libs/bootstrap/3.3.5/js/bootstrap.min',
        'd3': 'libs/d3/3.5.7/d3.min',
        'c3': 'libs/c3/0.6.14/c3.min',
        'leaflet': 'libs/leaflet/0.7.7/leaflet-src',
        'map-functionality': 'scripts/views/map/map',
        'leafletDraw': 'libs/leaflet.draw/0.2.3/leaflet.draw-src',
        'timePicker': 'libs/jquery.timepicker/1.10.0/jquery.timepicker.min'
    },
    shim: {
        leaflet: {
            exports: ['L']
        },
        'static/scripts/views/map/cluster.js': {
            deps: ['leaflet'],
        },
        leafletDraw: {
            deps: ['leaflet'],
            exports: 'LeafletDraw'
        },
        signals: {
            exports: ['signals']
        },
        crossroads: {
            deps: ['backbone', 'jquery', 'signals'],
            exports: ['crossroads']
        },
        'map-functionality': {
            deps: ['leaflet', 'leafletDraw']
        },
        bootstrap: {
            deps: ["jquery"]
        }
    }
});
require([
    'jquery',
    'bootstrap',
    'backbone',
    'underscore',
    'leaflet',
    'static/scripts/views/map/cluster.js',
    'map-functionality',
    'static/libs/select2-4.0.13/select2.min.js',
    'static/scripts/parameters.js',
    'static/scripts/shared.js',
    'static/scripts/views/statistic/view.js',
    'static/scripts/views/map-sidebar/country-list.js',
    'static/scripts/views/map-sidebar/healthsite-detail/control.js',
    'static/scripts/views/map-sidebar/shapefile-downloader.js',
    'static/scripts/views/navbar/search.js',
    'static/scripts/views/map/app.js',
    'static/scripts/helper.js',
], function ($, bootstrap, Backbone, _, L, Cluster, MAP, Select2, Parameters, Shared, CountryStatistic, CountryList, LocalityDetail, ShapefileDownloader, Search, App, Helper) {
    shared.dispatcher = _.extend({}, Backbone.Events);
    parameters = new Parameters();
    map = new MAP();

    new App();
    renderCredit();

    L.clusterLayer = new Cluster();

    var countryStatictic = new CountryStatistic();
    new CountryList();
    new LocalityDetail();
    var search = new Search();
    new ShapefileDownloader();

    // 1st step
    function goToCountry() {
        $("#locality-info").hide();
        if (parameters.get('country')) {
            $("#locality-statistic").show();
            $("#locality-info").hide();
            $("#locality-default").hide();
            countryStatictic.showStatistic(
                parameters.get('country'),
                function () {
                    $("#locality-info").hide();
                    goToPlace();
                }, function () {
                    $("#locality-info").hide();
                    goToPlace();
                });
        } else {
            countryStatictic.getCount("", function (data) {
                $('#healthsites-count').html(data);
                $('#healthsites-count').css('opacity', 1);
            });
            goToPlace();
        }
    }

    // 2rd step
    function goToPlace() {
        setTimeout(function () {
            if (parameters.get('place')) {
                search.placeSearchInit(
                    parameters.get('place'), function () {
                        goToLocality();
                    }, function () {
                        goToLocality();
                    });
            } else {
                goToLocality()
            }
        }, 100);
    }

    // 3rd step
    function goToLocality() {
        if (shared.currentID()) {
            var identifiers = shared.currentID().split('/');
            shared.dispatcher.trigger(
                'show-locality-detail', identifiers[0], identifiers[1]);
        } else if (shared.currentReviewID()) {
            shared.dispatcher.trigger(
                'show-locality-review', shared.currentReviewID());
        }
    }

    goToCountry();


    // geolocate
    function returnPosition(position) {
        shared.dispatcher.trigger('map.pan', {'location': [position.coords.latitude, position.coords.longitude]});
    }

    $('#geolocate').click(function () {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(returnPosition);
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    });

    $('#coordinate-input-form').submit(function (e) {
        e.preventDefault();
        var input = $('#coordinate-input').val();
        var coordinates = input.replaceAll(' ', '').split(',');
        if (coordinates.length === 2) {
            shared.dispatcher.trigger('map.setCenter', coordinates);
        }
    })
});