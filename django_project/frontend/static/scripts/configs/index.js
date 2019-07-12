require.config({
    baseUrl: '/static/',
    paths: {
        "jquery": "libs/jquery.js/3.3.1/jquery.min",
        "jquery-ui": "libs/jquery.js/1.12.1/jquery-ui.min",
        "backbone": "libs/backbone.js/1.4.0/backbone-min",
        "underscore": "libs/underscore.js/1.9.1/underscore-min",
        "bootstrap": "libs/bootstrap/3.3.5/js/bootstrap.min",
        "d3": "libs/d3/3.5.7/d3.min",
        "c3": "libs/c3/0.6.14/c3.min",
        "leaflet": "libs/leaflet/0.7.7/leaflet-src",
        'map-functionality': 'scripts/views/map/map',
        'leafletDraw': 'libs/leaflet.draw/0.2.3/leaflet.draw-src'
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
    }
});
require([
    'jquery',
    'backbone',
    'underscore',
    'leaflet',
    'static/scripts/views/map/cluster.js',
    'map-functionality',
    'static/scripts/parameters.js',
    'static/scripts/shared.js',
    'static/scripts/views/statistic/search.js',
    'static/scripts/views/statistic/view.js',
    'static/scripts/views/navbar/search.js',
    'static/scripts/views/map/app.js',
], function ($, Backbone, _, L, Cluster, MAP, Parameters, Shared, CountrySearch, CountryStatistic, Search, App) {
    shared.dispatcher = _.extend({}, Backbone.Events);
    parameters = new Parameters();
    map = new MAP();

    new App();
    L.clusterLayer = new Cluster();

    $(document).ready(function () {
        renderCredit();
    });

    // render country statistic view
    var countryStatictic = new CountryStatistic();
    countryStatictic.getCount("", function (data) {
        $('#healthsites-count').html(data);
        $('#healthsites-count').css('opacity', 1);
    });
    countryStatictic.showStatistic("");


    new CountrySearch();
    new Search();
});