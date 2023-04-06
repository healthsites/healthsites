define([
    'backbone',
    'jquery'], function (Backbone, $) {
    return Backbone.View.extend({
        url: api + "/facilities/",
        getHealthsite: function (osm_id, osm_type, successCallback, errorCallback) {
            $.ajax({
                url: this.url + osm_type + '/' + osm_id + "?output=geojson",
                dataType: 'json',
                success: function (data) {
                    if (successCallback) {
                        successCallback(data);
                    }
                },
                error: function (error) {
                    if (errorCallback) {
                        errorCallback(error)
                    }
                }
            });
        },
        getReview: function (review_id, successCallback, errorCallback) {
            $.ajax({
                url: api+'/pending/reviews/' + review_id,
                dataType: 'json',
                success: function (data) {
                    if (successCallback) {
                        successCallback(data);
                    }
                },
                error: function (error) {
                    if (errorCallback) {
                        errorCallback(error)
                    }
                }
            });
        }
    })
});

