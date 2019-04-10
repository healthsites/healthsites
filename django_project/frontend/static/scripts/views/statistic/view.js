define([
    'backbone',
    'jquery',
    'static/scripts/views/statistic/request.js',
    'static/scripts/views/statistic/chart.js',
    'static/scripts/views/statistic/pie.js'], function (Backbone, $, Request, Chart, Pie) {
    return Backbone.View.extend({
        initialize: function () {
            this.listenTo(shared.dispatcher, 'show-statistic', this.showStatistic);
            this.$localityNumber = $("#locality-number");
            this.$updateWrapper = $("#updates-wrapper");
            this.$title = $("#title");

            this.chart = new Chart('chart', 220, 18);
            this.pie = new Pie('piechart', 220);
            this.request = new Request();
        },
        showStatistic: function (country, callback) {
            var self = this;
            this.request.getStatistic(country, function (data) {
                if (callback) {
                    callback();
                }
                $APP.trigger('map.update-geoname', {'geoname': country});

                //{# default #}
                self.$localityNumber.html(0);
                self.$updateWrapper.html('<div id="updates-1" class="graph updates"><div class="entry">-</div></div>');

                //{# show the real data #}
                //{# country title #}
                if (country === "") {
                    country = "World";
                    self.$title.attr('href', "#");
                } else {
                    self.$title.attr('href', "map?country=" + country);
                }
                self.$title.html(country);

                //{# country healthsite number #}
                if (data.localities) {
                    self.$localityNumber.html(data.localities);
                    if (data.numbers) {
                        self.chart.update(data.localities, data.numbers);
                    }
                }
                if (data.completeness) {
                    self.pie.update(data.completeness.basic, data.completeness.partial, data.completeness.complete);
                }

                // Create latest updates data
                if (data.last_update.length > 0) {
                    self.$updateWrapper.html("");
                    $.each(data.last_update, function (i, update) {
                        var page = parseInt(i / 5);
                        var wrapper = $("#updates-" + page);
                        if (wrapper.length == 0) {
                            self.$updateWrapper.append('<div id="updates-' + page + '" class="graph updates"></div>');
                            wrapper = $("#updates-" + page);
                            if (page != 0) {
                                wrapper.hide();
                            }
                        }
                        var html = "<div class=\"entry\">";
                        html += "<div class=\"entry\">";
                        html += "<span class=\"date\">" + getDateString(update.changeset_timestamp) + "</span> - ";
                        html += "<span class=\"name\">";
                        html += "<a href=\"profile/" + update.changeset_user + "\">@" + update.changeset_user + "</a></span> - ";
                        var mode = "added";
                        if (update.changeset_version > 1) {
                            mode = "amended";
                        }

                        //{# update the html #}
                        html += "<a href=\"map#!/locality/" + update.locality_uuid + "\" class=\"location-name\">" + update.name + "</a>";
                        html += "<span class=\"location-name\"> " + mode + " </span>";
                        html += "</div>";
                        wrapper.append(html);
                    });
                    updateButton();
                }

                //{# set view port #}
                // creating polygon
                var polygon_raw = data.geometry;
                if (polygon_raw) {
                    var polygon_json = JSON.parse(polygon_raw);
                    var polygon = polygon_json['coordinates'];
                    $APP.trigger('map.create-polygon', {'polygon': polygon});
                }
                if (data.viewport) {
                    var northeast_lat = parseFloat(data.viewport.northeast_lat);
                    var northeast_lng = parseFloat(data.viewport.northeast_lng);
                    var southwest_lat = parseFloat(data.viewport.southwest_lat);
                    var southwest_lng = parseFloat(data.viewport.southwest_lng);
                    if (southwest_lat !== 0.0 && southwest_lng !== 0.0 && northeast_lat !== 0.0 && northeast_lng) {
                        map._setFitBound(southwest_lat, southwest_lng, northeast_lat, northeast_lng);
                        $APP.trigger('map.update-bound', {
                            'southwest_lat': southwest_lat,
                            'southwest_lng': southwest_lng,
                            'northeast_lat': northeast_lat,
                            'northeast_lng': northeast_lng
                        });
                    }
                }
                mapcount();
                $APP.trigger('map.rerender');
            });
        }
    })
});

