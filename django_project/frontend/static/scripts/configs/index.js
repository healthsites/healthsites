require(['./common'], function (common) {
    require([
        'backbone',
        'static/scripts/shared.js',
        'static/scripts/views/statistic/search.js',
        'static/scripts/views/statistic/view.js',
        'static/scripts/views/navbar/search.js',
        'cluster-layer',
        'map-functionality',
        'static/js/custom-functions.js'
    ], function (Backbone, Shared, CountrySearch, CountryStatistic, Search) {
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

        $(document).ready(function () {
            var map = new MAP();
            renderCredit();
        });
    });
});