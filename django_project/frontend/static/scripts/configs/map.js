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
    'static/scripts/views/map-sidebar/locality-detail.js',
    'static/scripts/views/map-sidebar/shapefile-downloader.js',
    'static/scripts/views/navbar/search.js'
], function (Backbone, _, Shared, CountryStatistic, CountryList, LocalityDetail, ShapefileDownloader, Search) {
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
    new ShapefileDownloader();

    function goToLocality() {
        if (identifier) {
            var identifiers = identifier.split('/');
            shared.dispatcher.trigger('show-locality-detail',
                {
                    'osm_type': identifiers[0],
                    'osm_id': identifiers[1]
                }
            );
        }
    }

    if (parameters['country']) {
        $("#locality-statistic").show();
        $("#locality-info").hide();
        $("#locality-default").hide();
        countryStatictic.showStatistic(
            parameters['country'],
            function () {
                goToLocality()
            });
    } else {
        if (identifier) {
            goToLocality();
        } else {
            countryStatictic.getCount("", function (data) {
                $('#healthsites-count').html(data);
            });
        }
    }
});