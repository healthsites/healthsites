define([
    'backbone',
    'jquery'], function (Backbone, $, Chart) {
    return Backbone.View.extend({
        url: "/api/v2/facilities/statistic",
        getStatistic: function (country, successCallback, errorCallback) {
            $.ajax({
                url: this.url,
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

