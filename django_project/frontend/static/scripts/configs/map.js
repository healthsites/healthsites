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
        'static/scripts/views/statistic/view.js',
        'static/scripts/views/map-sidebar/country-list.js',
        'static/scripts/views/map-sidebar/healthsite-detail/control.js',
        'static/scripts/views/map-sidebar/shapefile-downloader.js',
        'static/scripts/views/navbar/search.js',
        'static/scripts/views/map/app.js',
    ], function ($, Backbone, _, L, Cluster, MAP, Parameters, Shared, CountryStatistic, CountryList, LocalityDetail, ShapefileDownloader, Search, App) {
        shared.dispatcher = _.extend({}, Backbone.Events);
        parameters = new Parameters();
        map = new MAP();

        new App();
        renderCredit();

        L.clusterLayer = new Cluster();

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
                countryStatictic.getCount("", function (data) {
                    $('#healthsites-count').html(data);
                    $('#healthsites-count').css('opacity', 1);
                });
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
                    goToLocality()
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


        // geolocate
        function returnPosition(position) {
            shared.dispatcher.trigger('map.pan', {'location': [position.coords.latitude, position.coords.longitude]});
        }

        $('#geolocate').click(function () {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(returnPosition);
            } else {
                alert("Geolocation is not supported by this browser.");
            }
        });
    });
});
