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
                url: api + "/facilities/shapefile/" + this.country + '/detail',
                dataType: 'json',
                success: function (data) {
                    self.$el.html('<i>' + data['filename'] + ' (last update at : ' + new Date(data['time'] * 1000) + ')</i>');
                    self.$el.click(function () {
                        var url = api + "/facilities/shapefile/" + self.country + '/download';
                        if (window.hsAnalytics) {
                            window.hsAnalytics.event('file_download', {
                                file_name: self.country + '.zip',
                                file_extension: 'zip',
                                link_url: url,
                                country: self.country
                            });
                        }
                        window.location.href = url;
                    });
                },
                error: function () {
                    self.$el.html('<i>Shapefile is not found, please ask admin to generate it.</i>')
                }
            });
        }
    })
});

