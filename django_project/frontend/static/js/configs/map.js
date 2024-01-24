require.config(requireConfig);
require([
    'backbone',
    'underscore',
    'leaflet',
    'js/views/map/cluster',
    'js/views/map/map',
    'js/parameters',
    'js/shared',
    'js/views/statistic/view',
    'js/views/map-sidebar/country-list',
    'js/views/map-sidebar/healthsite-detail/control',
    'js/views/map-sidebar/shapefile-downloader',
    'js/views/map-sidebar/filter',
    'js/views/navbar/search',
    'js/views/map/app'
], function (Backbone, _, L, Cluster, MAP, Parameters, Shared, CountryStatistic, CountryList, LocalityDetail, ShapefileDownloader, Filter, Search, App) {
    shared.dispatcher = _.extend({}, Backbone.Events);
    parameters = new Parameters();
    map = new MAP();

    new App();
    renderCredit();

    L.clusterLayer = new Cluster();
    var countryStatictic = new CountryStatistic();
    new LocalityDetail();
    var search = new Search();
    new ShapefileDownloader();
    if (countries.length) {
        if (parameters.get('country')) {
            new Filter(true);
            new CountryList($('#locality-statistic #countries-table'), parameters.get('country'));
        } else {
            new Filter(false);
            new CountryList($('#countries-table'));
        }
    }

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
        } else if (shared.currentReviewID()) {
            shared.dispatcher.trigger(
                'show-locality-review', shared.currentReviewID());
        }
    }

    goToCountry();


    // geolocate
    function returnPosition(position) {
        shared.dispatcher.trigger('map.pan', { 'location': [position.coords.latitude, position.coords.longitude] });
    }

    $('#geolocate').click(function () {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(returnPosition);
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    });

    $('#coordinate-input-form').submit(function (e) {
        e.preventDefault();
        var input = $('#coordinate-input').val();
        var coordinates = input.replaceAll(' ', '').split(',');
        if (coordinates.length === 2) {
            shared.dispatcher.trigger('map.setCenter', coordinates);
        }
    })
});