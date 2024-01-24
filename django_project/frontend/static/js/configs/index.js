require.config(requireConfig);
require([
    'jquery',
    'backbone',
    'underscore',
    'leaflet',
    'js/views/map/cluster',
    'js/views/map/map',
    'js/parameters',
    'js/shared',
    'js/views/statistic/search',
    'js/views/statistic/view',
    'js/views/navbar/search',
    'js/views/map/app',
], function ($, Backbone, _, L, Cluster, MAP, Parameters, Shared, CountrySearch, CountryStatistic, Search, App) {
    shared.dispatcher = _.extend({}, Backbone.Events);
    parameters = new Parameters();
    map = new MAP();

    new App();
    L.clusterLayer = new Cluster();

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