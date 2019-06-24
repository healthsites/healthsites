require.config({
    baseUrl: '/static/',
    paths: {
        "jquery": "libs/jquery.js/3.3.1/jquery.min",
        "jquery-ui": "libs/jquery.js/1.12.1/jquery-ui.min",
        "backbone": "libs/backbone.js/1.4.0/backbone-min",
        "underscore": "libs/underscore.js/1.9.1/underscore-min",
        "bootstrap": "libs/bootstrap/3.3.5/js/bootstrap.min",
        "d3": "libs/d3/3.5.7/d3.min",
        "c3": "libs/c3/0.4.22/c3.min",
        "leaflet": "libs/leaflet/0.7.7/leaflet-src",
        "slickmin": "libs/jquery.slick/1.5.7/slick.min",
        "leafletDraw": "libs/leaflet.draw/0.2.3/leaflet.draw-src",
        "signals": "libs/js-signals/1.0.0/js-signals.min",
        "app": "js/app",
        "cluster-layer": "js/cluster-layer",
        "map-functionality": "js/map-functionality",
        "hasher": "libs/hasher/1.2.0/hasher.min",
        "crossroads": "libs/crossroads/0.12.2/crossroads.min",
    },
    shim: {
        jquery : {
            exports: ['$', 'jQuery']
        },
        "jquery-ui" : {
            exports: ['jqueryUI']
        },
        bootstrap : {
            deps : [ 'jquery'],
            exports: 'Bootstrap'
        },
        underscore : {
            exports : '_'
        },
        backbone : {
            deps : [ 'jquery', 'underscore' ],
            exports : 'Backbone'
        },
        leaflet : {
            exports: ['L']
        },
        leafletDraw : {
            deps : [ 'leaflet'],
            exports: 'LeafletDraw'
        },
        slickmin : {
            exports: [ 'slickMin' ]
        },
        signals : {
            exports: [ 'signals' ]
        },
        crossroads: {
            deps: ['backbone', 'jquery', 'signals'],
            exports: ['crossroads']
        },
        'cluster-layer': {
            deps : [ 'leaflet'],
        },
        'map-functionality': {
            deps : [ 'leaflet', 'cluster-layer', 'leafletDraw' ]
        },
    }
});