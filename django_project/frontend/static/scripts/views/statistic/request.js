define([
    'backbone',
    'jquery'], function (Backbone, $) {
    return Backbone.View.extend({
        url: "/api/v2/facilities/",
        getStatistic: function (country, successCallback, errorCallback) {
            $.ajax({
                url: this.url + 'statistic',
                dataType: 'json',
                data: {
                    country: country
                },
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
        getCount: function (country, successCallback, errorCallback) {
            $.ajax({
                url: this.url + 'count',
                dataType: 'json',
                data: {
                    country: country
                },
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

