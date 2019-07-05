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
    }
});
require([
    'backbone',
    'underscore',
    'static/scripts/shared.js',
    'static/scripts/views/statistic/view.js',
    'static/scripts/views/map-sidebar/country-list.js',
    'static/scripts/views/map-sidebar/healthsite-detail/control.js',
    'static/scripts/views/map-sidebar/shapefile-downloader.js',
    'static/scripts/views/navbar/search.js'
], function (Backbone, _, Shared, CountryStatistic, CountryList, LocalityDetail, ShapefileDownloader, Search) {
    shared.dispatcher = _.extend({}, Backbone.Events);
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
                goToPlace()
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