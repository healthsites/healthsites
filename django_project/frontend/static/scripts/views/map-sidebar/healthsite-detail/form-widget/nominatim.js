define([
    'backbone',
    'jquery'], function (Backbone, $) {
    return Backbone.View.extend({
        // the zoom indicator what level on nominatim
        COUNTRY: {
            ZOOM: 3,
            LIST: null
        },
        STATE: {
            ZOOM: 5,
            LIST: null
        },
        COUNTY: {
            ZOOM: 8,
            LIST: null
        },
        CITY: {
            ZOOM: 10,
            LIST: null,
            KEYS: ['city', 'village', 'distric', 'state_district']
        },
        SUBURB: {
            ZOOM: 14,
            LIST: null
        },
        MAJOR_STREETS: {
            ZOOM: 16,
            LIST: null
        },
        MAJOR_AND_MINOR_STREETS: {
            ZOOM: 17,
            LIST: null
        },
        BUILDING: {
            ZOOM: 16,
            LIST: null
        },
        URL: 'https://nominatim.openstreetmap.org/reverse',

        lat: null,
        lon: null,
        initialize: function () {
            this.updateLocation(null, null);
        },
        /**
         * Update current latitude and longitude
         * @param lat = float
         * @param lon = float
         */
        updateLocation: function (lat, lon) {
            this.lat = lat;
            this.lon = lon;

            // update all list to be null
            this.COUNTRY.LIST = null;
            this.STATE.LIST = null;
            this.COUNTY.LIST = null;
            this.CITY.LIST = null;
            this.SUBURB.LIST = null;
            this.MAJOR_STREETS.LIST = null;
            this.MAJOR_AND_MINOR_STREETS.LIST = null;
            this.BUILDING.LIST = null;
        },
        /**
         * Get cities from nominatim
         * passing data using success callback
         * The indicator selected
         * @param KEY = the key that will be checked
         * @param successCallback
         * @param errorCallback
         */
        getData: function (KEY, successCallback, errorCallback) {
            if (!KEY.hasOwnProperty('LIST') || !KEY.hasOwnProperty('ZOOM')) {
                throw "The KEY is not recognized";
            }
            let data = KEY.LIST;
            if (data == null) {
                $.ajax({
                    url: this.URL,
                    type: 'GET',
                    data: {
                        lat: this.lat,
                        lon: this.lon,
                        format: 'json',
                        zoom: KEY.ZOOM
                    },
                    success: function (data) {
                        KEY.LIST = data;
                        successCallback(KEY.LIST)
                    },
                    error: function (error) {
                        errorCallback(error);
                    }
                });
            } else {
                successCallback(data);
            }

            return data
        }
    })
});

