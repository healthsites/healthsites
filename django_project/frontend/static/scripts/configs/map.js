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
        'map-functionality': 'scripts/views/map',
        'leafletDraw': 'libs/leaflet.draw/0.2.3/leaflet.draw-src'
    },
    shim: {
        leaflet : {
            exports: ['L']
        },
        'static/scripts/views/cluster.js': {
            deps : [ 'leaflet'],
        },
        leafletDraw : {
            deps : [ 'leaflet'],
            exports: 'LeafletDraw'
        },
        signals : {
            exports: [ 'signals' ]
        },
        crossroads: {
            deps: ['backbone', 'jquery', 'signals'],
            exports: ['crossroads']
        },
        'map-functionality': {
            deps : [ 'leaflet', 'leafletDraw' ]
        },
    }
});
require([
    'jquery',
    'backbone',
    'underscore',
    'leaflet',
    'static/scripts/views/cluster.js',
    'map-functionality',
    'static/scripts/parameters.js',
    'static/scripts/shared.js',
    'static/scripts/views/statistic/view.js',
    'static/scripts/views/map-sidebar/country-list.js',
    'static/scripts/views/map-sidebar/healthsite-detail/control.js',
    'static/scripts/views/map-sidebar/shapefile-downloader.js',
    'static/scripts/views/navbar/search.js',
    'static/scripts/views/app.js',
], function ($, Backbone, _, L, Cluster, MAP, Parameters, Shared, CountryStatistic, CountryList, LocalityDetail, ShapefileDownloader, Search, App) {
    var parameters = new Parameters();
    shared.dispatcher = _.extend({}, Backbone.Events);

    var APP = new App();
    var map = new MAP();
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
        }
    }

    goToCountry();
});