define([
    'backbone',
    'jquery'], function (Backbone, $) {
    return Backbone.View.extend({
        found: false,
        initialize: function () {
            this.$el = $('.shapefile-downloader');

            this.country = parameters.get('country');
            if (!parameters.get('country')) {
                this.country = 'World';
            }

            this.checkingShapefile();
        },
        checkingShapefile: function () {
            var self = this;
            $.ajax({
                url: "/api/v2/facilities/shapefile/" + this.country + '/detail',
                dataType: 'json',
                success: function (data) {
                    self.$el.html('<i>' + data['filename'] + ' (last update at : ' + new Date(data['time'] * 1000) + ')</i>');
                    self.$el.click(function () {
                        window.location.href = "/api/v2/facilities/shapefile/" + self.country + '/download';
                    });
                },
                error: function () {
                    self.$el.html('<i>Shapefile is not found, please ask admin to generate it.</i>')
                }
            });
        }
    })
});

