require(['./common'], function (common) {
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
});