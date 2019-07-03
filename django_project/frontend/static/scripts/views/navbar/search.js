define([
    'backbone',
    'jquery',
    'jquery-ui', 'bootstrap'], function (Backbone, $, JqueryUI, Bootstrap) {
    return Backbone.View.extend({
        autocomplete_localities: "/api/v2/facilities/autocomplete/",
        autocomplete_country: "/api/v2/countries/autocomplete/e",
        autocomplete_url: '',
        initialize: function () {
            var self = this;
            this.currentSearch = 'healthsite';
            self.autocomplete_url = self.autocomplete_localities;
            var $navbarSearch = $('.navbar-search');
            var $searchbox = $("#search-box");
            this.el = $('#search-form');
            this.el.find('input:radio[name=option]').change(function () {
                $("#search-box").val("");
                // set data for autocomplete
                self.currentSearch = this.value;
                if (this.value === 'country') {
                    self.autocomplete_url = self.autocomplete_country;
                } else if (this.value === 'healthsite') {
                    self.autocomplete_url = self.autocomplete_localities;
                }
            });

            // searchbar toggler
            $navbarSearch.click(function () {
                $("body").toggleClass("searchbar-active");
                $navbarSearch.find('i').toggleClass("fa-search fa-times");
                mapcount();
            });

            // search autocomplete
            $searchbox.autocomplete({
                source: function (request, response) {
                    $searchbox.css("cursor", "wait");
                    $.ajax({
                        url: self.autocomplete_url,
                        data: {
                            q: request.term
                        },
                        success: function (data) {
                            response(data);
                            $searchbox.css("cursor", "");
                        },
                        error: function (request, error) {
                            $searchbox.css("cursor", "");
                        },
                    });
                },
                minLength: 3,
                select: function (event, ui) {
                    if (self.currentSearch === 'healthsite') {
                        window.location = '/map#!/locality/' + ui.item.id;
                    } else if (self.currentSearch === 'country') {
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
        }
    })
});

