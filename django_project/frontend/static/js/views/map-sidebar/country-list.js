define([
    'backbone',
    'jquery',
    'jquery-ui',
    'js/views/statistic/request'], function (Backbone, $, JqueryUI, Request) {
    return Backbone.View.extend({
        headers: ["A - E", "F - J", "K - O", "P - T", "U - Z"],
        rowRegex: [/[a-e]/, /[f-j]/, /[k-o]/, /[p-t]/, /[u-z]/],
        initialize: function ($element, parent) {
            this.$element = $element;
            this.request = new Request();
            this.parent = parent;
            this.render();
        },
        /** Return id for a country name
         * @param countryName
         * @returns {string}
         */
        countryID: function (countryName) {
            if (countryName) {
                var country_id = countryName.split(".").join("-");
                country_id = country_id.split("&#39;").join("-");
                country_id = country_id.split(" ").join("-");
                country_id = country_id.split("(").join("-");
                country_id = country_id.split(")").join("-");
                return country_id;
            }
        },
        /** Render all country list
         */
        render: function () {
            var self = this;
            var htmlData = {}
            let $country_table = this.$element.find('#accordion-country')

            // create html for title
            $.each(countries, function (i, country) {
                // if parent is none, skip it
                if (country.parent === 'None') {
                    return
                }

                // if parent of parameter is not empty
                // and country.parent is not same with parent, skip it
                if (self.parent && country.parent !== self.parent) {
                    return
                }

                // render parent title
                if (!htmlData[country.parent]) {
                    htmlData[country.parent] = {
                        countries: [],
                        countriesHtml: []
                    }
                }
                var countryID = self.countryID(country.name);
                htmlData[country.parent].countries.push(country.name);
                htmlData[country.parent].countriesHtml.push(
                    '<div class="block-data">' +
                    '   <span class="col-xs-6">' +
                    '       <a href="map?country=' + country.name + '">' + country.name + '</a>' +
                    '   </span> ' +
                    '   <span id="' + countryID + '-number" class="col-xs-3"></span>' +
                    '   <span id="' + countryID + '-complete" class="col-xs-3"></span>' +
                    '</div>')
            })

            // create html for members
            let keys = Object.keys(htmlData).sort()
            if (keys.length === 0) {
                this.$element.remove()
            }
            $.each(keys, function (i, continent) {
                let countriesData = htmlData[continent];

                // if parent is none, create accordion
                if (!self.parent) {
                    var continentID = self.countryID(continent);
                    var html =
                        '<h3 id="country-group-' + continentID + '">' +
                        '<div class="block-data">' +
                        '   <span class="col-xs-6">' +
                        '       <a href="map?country=' + continent + '">' + continent + '</a>' +
                        '   </span> ' +
                        '   <span id="' + continentID + '-number" class="col-xs-3"></span>' +
                        '   <span id="' + continentID + '-complete" class="col-xs-3"></span>' +
                        '</div>'
                        + '</h3>';
                    html += '<div class="table">';
                    html += countriesData.countriesHtml.join('');
                    html += '</div>';
                    $country_table.append(html);

                    // create headers of country
                    var $header = $("#country-group-" + continentID);
                    $header.data('countries', countriesData.countries);
                    $header.find('a').click(function () {
                        document.location = $(this).attr('href')
                        return false
                    })
                    $header.click(function () {
                        self.loadData($(this).data('countries'));
                    })

                    // load statistic
                    self.getStatisticData(continent)
                } else {
                    html = '<div class="table">';
                    html += countriesData.countriesHtml.join('');
                    html += '</div>';
                    $country_table.append(html);
                    self.loadData(countriesData.countries);
                }
            })

            $(".accordion").accordion({
                collapsible: true,
                header: "h3",
                active: false,
            });
            $('.ui-accordion-content').css('height', 'auto');
        },
        /** Return statistic data for country
         * @param country
         */
        getStatisticData: function (country) {
            var countryID = this.countryID(country);
            var $number = $('#' + countryID + '-number');
            var $complete = $('#' + countryID + '-complete');
            if (!$number.html()) {
                $number.html('loading');
                $complete.html('loading');
                this.request.getCount(country, function (data) {
                    $number.html(data);
                    $complete.html(0.0);
                });
            }
        },
        /** Load every countries for statistic data
         * @param element
         */
        loadData: function (countries) {
            var self = this;
            $.each(countries, function (i, country) {
                self.getStatisticData(country)
            });
        }
    })
});

