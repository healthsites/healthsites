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
        "leaflet": "https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/leaflet-src",
        "slickmin": "https://cdn.jsdelivr.net/jquery.slick/1.5.7/slick.min",
        "leafletDraw": "https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/0.2.3/leaflet.draw-src",
        "jsSignal": "https://cdnjs.cloudflare.com/ajax/libs/js-signals/1.0.0/js-signals.min",
    }
});
require([
    'backbone',
    'underscore',
    'jquery',
    'jquery-ui',
    'bootstrap',
    'leaflet',
    'slickmin',
    'leafletDraw',
    'jsSignal',
    'd3',
    'c3',
    'scripts/shared.js',
    'scripts/views/statistic/search.js',
    'scripts/views/statistic/view.js',
    'scripts/views/navbar/search.js'
], function (Backbone, _, $, jqueryUI, bootstrap, L, slickMin, LeafletDraw, jsSignal, d3, c3, Shared, CountrySearch, CountryStatistic, Search) {
    shared.dispatcher = _.extend({}, Backbone.Events);

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