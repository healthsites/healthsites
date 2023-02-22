define([
    'backbone',
    'jquery',
    'jquery-ui'], function (Backbone, $, JqueryUI) {
    return Backbone.View.extend({
        autocomplete_localities: "/api/v3/facilities/autocomplete/",
        autocomplete_country: "/api/v3/countries/autocomplete/",
        autocomplete_url: '',
        geoname_search: "/api/v3/gmaps/search/geoname",
        initialize: function () {
            var self = this;
            this.currentSearch = 'healthsite';
            self.autocomplete_url = self.autocomplete_localities;
            var $navbarSearch = $('.navbar-search');
            this.$searchbox = $("#search-box");
            this.el = $('#search-form');

            this.el.submit(function () {
                if (!self.autocomplete_url) {
                    self.sendToAnalytic(self.$searchbox.val())
                    self.placeSearch(self.$searchbox.val());
                    return false;
                }
                return false;
            });
            this.el.find('input:radio[name=option]').change(function () {
                self.searchBoxFinished();
                self.$searchbox.val('');
                // set data for autocomplete
                self.currentSearch = this.value;
                if (this.value === 'country') {
                    self.autocomplete_url = self.autocomplete_country;
                } else if (this.value === 'healthsite') {
                    self.autocomplete_url = self.autocomplete_localities;
                } else {
                    self.autocomplete_url = null;
                }
            });

            // searchbar toggler
            $navbarSearch.click(function () {
                $("body").toggleClass("searchbar-active");
                $navbarSearch.find('i').toggleClass("fa-search fa-times");
                mapcount();
            });

            $('#search-text').click(function () {
                if (!$("#search-form").is(":visible")) {
                    $("body").toggleClass("searchbar-active");
                    $navbarSearch.find('i').toggleClass("fa-search fa-times");
                    mapcount();
                }
            });

            // search autocomplete
            this.$searchbox.autocomplete({
                source: function (request, response) {
                    self.$searchbox.removeClass('error');
                    if (self.autocomplete_url) {
                        self.searchBoxSubmitted();
                        self.sendToAnalytic(request.term)
                        self.searchAjax = $.ajax({
                            url: self.autocomplete_url,
                            data: {
                                q: request.term
                            },
                            success: function (data) {
                                response(data);
                                self.searchBoxFinished();
                            },
                            error: function (request, error) {
                                self.searchBoxFinished();
                            },
                        });
                    }
                },
                minLength: 3,
                select: function (event, ui) {
                    if (self.currentSearch === 'healthsite') {
                        self.sendToAnalytic(`${ui.item.label} (${ui.item.id})`)
                        window.location = '/map#!/locality/' + ui.item.id;
                    } else if (self.currentSearch === 'country') {
                        self.sendToAnalytic(ui.item.label)
                        window.location = '/map?country=' + ui.item.label;
                    }
                },
                open: function () {
                    $(this).removeClass("ui-corner-all").addClass("ui-corner-top");
                },
                close: function () {
                    $(this).removeClass("ui-corner-top").addClass("ui-corner-all");
                }
            });
        },
        searchBoxSubmitted: function () {
            this.$searchbox.removeClass('error');
            this.$searchbox.css("cursor", "wait");
        },
        searchBoxFinished: function () {
            this.$searchbox.css("cursor", "");
        },
        searchBoxError: function (error) {
            this.$searchbox.css("cursor", "");
            this.$searchbox.addClass('error');
        },
        placeSearchInit: function (geoname, successCallback, errorCallback) {
            $('#radio-place').click();
            this.$searchbox.val(geoname);
            this.placeSearch(geoname, successCallback, errorCallback);
        },
        placeSearch: function (geoname, successCallback, errorCallback) {
            var self = this;
            if (this.searchAjax) {
                this.searchAjax.abort()
            }
            if (geoname.length < 3) {
                self.searchBoxError();
                return;
            }
            // redirect into map if not map
            if (window.location.pathname !== '/map') {
                window.location = '/map?place=' + geoname;
                return false;
            } else {
                parameters.set('place', geoname);
            }
            this.searchBoxSubmitted();
            this.searchAjax = $.ajax({
                url: this.geoname_search,
                dataType: 'json',
                data: {
                    q: this.$searchbox.val()
                },
                success: function (data) {
                    self.searchBoxFinished();
                    shared.dispatcher.trigger('map.update-bound', {
                        'southwest_lat': data['southwest']['lat'],
                        'southwest_lng': data['southwest']['lng'],
                        'northeast_lat': data['northeast']['lat'],
                        'northeast_lng': data['northeast']['lng']
                    });
                    if (successCallback) {
                        successCallback(data);
                    }
                },
                error: function (error) {
                    self.searchBoxError()
                    if (errorCallback) {
                        errorCallback(error)
                    }
                }
            });
        },
        sendToAnalytic: function (value) {
            const searchValue = `${$('input:radio[name=option]:checked').val()}=${value}`;
            ga('send', 'event', 'search', searchValue);
        }
    })
});

