define([
    'backbone',
    'jquery'], function (Backbone, $, Chart) {
    return Backbone.View.extend({
        url: "/api/v2/facilities/statistic",
        getStatistic: function (country, callback) {
            $.ajax({
                url: this.url,
                dataType: 'json',
                data: {
                    country: country
                },
                success: function (data) {
                    if (callback) {
                        callback(data);
                    }
                }
            });
        }
    })
});

