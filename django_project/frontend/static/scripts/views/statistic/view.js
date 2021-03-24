define([
    'backbone',
    'jquery',
    'static/scripts/views/statistic/request.js',
    'static/scripts/views/statistic/chart.js',
    'static/scripts/views/statistic/pie.js'], function (Backbone, $, Request, Chart, Pie) {
    return Backbone.View.extend({
        initialize: function () {
            this.listenTo(shared.dispatcher, 'show-statistic', this.showStatistic);
            this.listenTo(shared.dispatcher, 'statistic.rerender', this.rerenderStatistic);
            this.$localityNumber = $("#locality-number");
            this.$updateWrapper = $("#updates-wrapper");
            this.$title = $("#title");

            this.chart = new Chart('chart', 220, 18);
            this.pie = new Pie('piechart', 220);
            this.request = new Request();
        },
        getCount: function (country, successCallback, errorCallback) {
            this.request.getCount(country, successCallback, errorCallback);
        },
        getStatistic: function (country, successCallback, errorCallback) {
            this.request.getStatistic(country, successCallback, errorCallback);
        },
        rerenderStatistic: function () {
            this.showStatistic(this.country, null, null, true);
        },
        showStatistic: function (country, successCallback, errorCallback, rerender) {
            var self = this;
            self.country = country;
            this.getStatistic(country, function (data) {
                shared.dispatcher.trigger('map.update-geoname', { 'geoname': country });

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
                    if (data.completeness) {
                        data.completeness['partial'] = data.localities - data.completeness['basic'] - data.completeness['complete'];
                        self.pie.update(data.completeness.basic, data.completeness.partial, data.completeness.complete);
                    }
                }

                // Create latest updates data
                if (data.last_update.length > 0) {
                    self.$updateWrapper.html("");
                    $.each(data.last_update, function (i, update) {
                        var page = parseInt(i / 5);
                        var $page = $("#updates-" + page);
                        if ($page.length === 0) {
                            self.$updateWrapper.append('<div id="updates-' + page + '" class="graph updates"></div>');
                            $page = $("#updates-" + page);
                            if (page !== 0) {
                                $page.hide();
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
                        html += "<a href=\"/map#!/locality/" + update.uuid + "\" class=\"location-name\">" + update.name + "</a>";
                        html += "<span class=\"location-name\"> " + mode + " </span>";
                        html += "</div>";
                        $page.append(html);
                    });
                    updateButton();
                }

                //{# set view port #}
                // creating polygon
                var polygon_raw = data.geometry;
                if (polygon_raw && !rerender) {
                    var polygon_json = JSON.parse(polygon_raw);
                    var polygon = polygon_json['coordinates'];
                    shared.dispatcher.trigger('map.create-polygon', { 'polygon': polygon });
                }
                if (data.viewport) {
                    var northeast_lat = parseFloat(data.viewport.northeast_lat);
                    var northeast_lng = parseFloat(data.viewport.northeast_lng);
                    var southwest_lat = parseFloat(data.viewport.southwest_lat);
                    var southwest_lng = parseFloat(data.viewport.southwest_lng);
                    if (southwest_lat !== 0.0 && southwest_lng !== 0.0 && northeast_lat !== 0.0 && northeast_lng) {
                        map._setFitBound(southwest_lat, southwest_lng, northeast_lat, northeast_lng);
                        if (!rerender) {
                            shared.dispatcher.trigger('map.update-bound', {
                                'southwest_lat': southwest_lat,
                                'southwest_lng': southwest_lng,
                                'northeast_lat': northeast_lat,
                                'northeast_lng': northeast_lng
                            });
                        }
                    }
                }
                mapcount();
                shared.dispatcher.trigger('map.rerender');

                // call callback
                if (successCallback) {
                    successCallback(data);
                }
            }, errorCallback);
        }
    })
});

