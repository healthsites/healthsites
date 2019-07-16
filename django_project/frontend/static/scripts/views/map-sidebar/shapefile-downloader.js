define([
    'backbone',
    'jquery',
    'jquery-ui',
    'bootstrap'], function (Backbone, $, JqueryUI, Bootstrap) {
    return Backbone.View.extend({
        initialize: function () {
            var self = this;
            this.$el = $('.shapefile-downloader');
            this.$el.click(function () {
                self.downloadShapefile();
            })
        },
        downloadShapefile: function () {
            if (this.$el.html() === 'shapefile') {
                this.$el.html('<i>generating...</i>');
                this.checkingShapefile();
            }
        },
        checkingShapefile: function () {
            var self = this;
            var country = parameters.get('country');
            if (!parameters.get('country')) {
                country = 'World';
            }
            $.ajax({
                url: "/api/v2/facilities/shapefile/process/" + country,
                dataType: 'json',
                success: function (data) {
                    if (!data['index'] || data['index'] !== data['total']) {
                        if (data['index']) {
                            self.$el.html('<i>' + data['index'] + '/' + data['total'] + '</i>');
                        }
                        setTimeout(
                            function () {
                                self.checkingShapefile();
                            }, 1000);
                    } else {
                        self.$el.html('shapefile');
                        window.location.href = '/data/shapefiles/' + country + '.zip';
                    }
                }
            });
        }
    })
});

