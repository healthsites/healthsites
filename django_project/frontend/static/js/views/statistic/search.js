
define([
    'backbone', 'jquery'], function (Backbone, $) {
    return Backbone.View.extend({
        url: api + "/countries/autocomplete/",
        initialize: function () {
            var self = this;
            this.el = $('#country-form');

            // Create autocomplete
            $(this.el).find('input').autocomplete({
                source: function (request, response) {
                    $.ajax({
                        url: self.url,
                        dataType: 'json',
                        data: {
                            q: request.term
                        },
                        success: function (data) {
                            response(data);
                        }
                    });
                },
                minLength: 3,
                select: function (event, ui) {
                    $(self.el).find('input').val(ui.item.value);
                    self.el.submit();
                },
                open: function () {
                    $(this).removeClass("ui-corner-all").addClass("ui-corner-top");
                },
                close: function () {
                    $(this).removeClass("ui-corner-top").addClass("ui-corner-all");
                }
            });

            // Submiting form country search
            this.el.submit(function (event) {
                var $searchIcon = $(this).find('.fa-search');
                var $input = $(this).find('input');
                var country = $input.val();
                event.preventDefault();
                $input.prop("disabled", true);

                $searchIcon.removeClass('fa-search');
                $searchIcon.addClass('fa-circle-o-notch');
                $searchIcon.addClass('fa-spin');
                shared.dispatcher.trigger('show-statistic', country,
                    function () {
                        $input.prop("disabled", false);
                        $searchIcon.addClass('fa-search');
                        $searchIcon.removeClass('fa-circle-o-notch');
                        $searchIcon.removeClass('fa-spin');
                    });

            });


        }
    })
});
