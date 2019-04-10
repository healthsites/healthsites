require.config({
    baseUrl: '/static/',
    paths: {
        "jquery": "libs/jquery.js/3.3.1/jquery.min",
        "jquery-ui": "libs/jquery.js/1.12.1/jquery-ui.min",
        "backbone": "libs/backbone.js/1.4.0/backbone-min",
        "underscore": "libs/underscore.js/1.9.1/underscore-min",
        "d3": "libs/d3/3.5.7/d3.min",
        "c3": "libs/c3/0.6.14/c3.min",
    }
});
require([
    'backbone',
    'underscore',
    'static/scripts/shared.js',
    'static/scripts/views/statistic/search.js',
    'static/scripts/views/statistic/view.js'

], function (Backbone, _, Shared, CountrySearch, CountryStatistic) {
    shared.dispatcher = _.extend({}, Backbone.Events);

    // render country statistic view
    var countryStatictic = new CountryStatistic();
    countryStatictic.showStatistic("");

    new CountrySearch();
});