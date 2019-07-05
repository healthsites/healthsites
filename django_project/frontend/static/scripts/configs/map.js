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
        'map-functionality': 'scripts/views/map-functionality',
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
    'static/scripts/shared.js',
    'static/scripts/views/statistic/view.js',
    'static/scripts/views/map-sidebar/country-list.js',
    'static/scripts/views/map-sidebar/healthsite-detail/control.js',
    'static/scripts/views/map-sidebar/shapefile-downloader.js',
    'static/scripts/views/navbar/search.js',
    'static/scripts/views/app.js',
], function ($, Backbone, _, L, Cluster, MAP, Shared, CountryStatistic, CountryList, LocalityDetail, ShapeFileDownloader, Search, App) {
    var APP;
    if (typeof APP == 'undefined') {
        APP = {};
        $APP = $(APP);
    }

    APP = new App();
    var map = new MAP();
    renderCredit();

    L.clusterLayer = new Cluster();

    shared.dispatcher = _.extend({}, Backbone.Events);
    var countryStatictic = new CountryStatistic();
    var identifier = shared.currentID();
    new CountryList();
    new LocalityDetail();
    var search = new Search();
    if (parameters['geoname']) {
        shared.replaceGeonameSearch('');
        search.placeSearchInit(parameters['geoname']);
    }
    new ShapeFileDownloader();

    function goToLocality() {
        if (identifier) {
            var identifiers = identifier.split('/');
            shared.dispatcher.trigger('show-locality-detail', identifiers[0], identifiers[1]);
        }
    }

    if (parameters['country']) {
        $('#locality-statistic').show();
        $('#locality-info').hide();
        $('#locality-default').hide();
        countryStatictic.showStatistic(
            parameters['country'],
            function () {
                $('#locality-info').hide();
                goToLocality()
            });
    } else {
        if (identifier) {
            goToLocality();
        } else {
            $('#locality-info').hide();
            countryStatictic.getCount('', function (data) {
                $('#healthsites-count').html(data);
            });
        }
    }
});