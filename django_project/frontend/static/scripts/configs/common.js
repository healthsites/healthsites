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