define([
    'backbone',
    'jquery',
    'jquery-ui',
    'bootstrap',
    'static/scripts/views/statistic/request.js'], function (Backbone, $, JqueryUI, Bootstrap, Request) {
    return Backbone.View.extend({
        headers: ["A - E", "F - J", "K - O", "P - T", "U - Z"],
        rowRegex: [/[a-e]/, /[f-j]/, /[k-o]/, /[p-t]/, /[u-z]/],
        initialize: function () {
            this.showListCountry();
            this.request = new Request();
        },
        countryID: function (countryName) {
            var country_id = countryName.split(".").join("-");
            country_id = country_id.split("&#39;").join("-");
            country_id = country_id.split(" ").join("-");
            country_id = country_id.split("(").join("-");
            country_id = country_id.split(")").join("-");
            return country_id;
        },
        showListCountry: function () {
            var self = this;
            var $country_table = $('#accordion-country');
            $.each(this.headers, function (index, header) {
                var countriesHtml = "";
                var found = false;
                var countriesFound = [];
                $.each(countries, function (i, country) {
                    var countryID = self.countryID(country);
                    if (country.toLowerCase()[0].match(self.rowRegex[index]) != null) {
                        found = true;
                        countriesHtml += '' +
                            '<div class="block-data">' +
                            '   <span class="col-xs-6">' +
                            '       <a href="map?country=' + country + '">' + country + '</a>' +
                            '   </span> ' +
                            '   <span id="' + countryID + '-number" class="col-xs-3"></span>' +
                            '   <span id="' + countryID + '-complete" class="col-xs-3"></span>' +
                            '</div>';
                        countriesFound.push(country);
                    } else {
                        if (found) return true;
                    }
                });

                // accordion html
                var html = '<h3 id="country-group-' + index + '">' + header + '</h3>';
                html += '<div class="table">';
                html += countriesHtml;
                html += '</div>';
                $country_table.append(html);
                var $header = $("#country-group-" + index);
                $header.data('countries', countriesFound);
                $header.click(function () {
                    self.loadData(this);
                })
            });

            $(".accordion").accordion({
                collapsible: true,
                header: "h3",
                active: false,
            });
            $('.ui-accordion-content').css('height', 'auto');
        },
        loadData: function (element) {
            var self = this;
            $.each($(element).data('countries'), function (i, country) {
                var countryID = self.countryID(country);
                var $number = $('#' + countryID + '-number');
                var $complete = $('#' + countryID + '-complete');
                if (!$number.html()) {
                    $number.html('loading');
                    $complete.html('loading');
                    self.request.getCount(country, function (data) {
                        $number.html(data);
                        $complete.html(0.0);
                    });
                }
            });
        }
    })
});

