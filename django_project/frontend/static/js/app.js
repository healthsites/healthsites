if (typeof APP == 'undefined') {
    APP = {};
    $APP = $(APP);
}

window.APP = (function () {
    "use strict";
    // private variables and functions

    // constructor
    var module = function () {
        // init map
        new MAP();

        // init localityModal
        new LocalityModal();

        this._initAPPEvents();

        this._bindExternalEvents();

        var myRe = /\/(\d+)\//i;
        var id = window.location.pathname.match(/\/([0-9]+)\//i);
        if (id) {
            $APP.trigger('locality.map.click', {'locality_id': id[1]});
        }

    };

    // prototype
    module.prototype = {
        constructor: module,

        _bindExternalEvents: function () {
            $APP.on('map.new_locality.point', function (evt) {
                var loc_button = $('#new_locality');

                if (loc_button.hasClass('btn-warning')) {
                    loc_button.toggleClass('btn-warning btn-danger');
                    loc_button.button('savelocality');
                }
            });

            $APP.on('locality.created', function (evt, payload) {
                var loc_button = $('#new_locality');

                loc_button.toggleClass('btn-default btn-danger');
                loc_button.button('toggle');
                loc_button.button('reset');
            });
        },

        _initAPPEvents: function () {
            $('#new_locality').on('click', function (evt) {
                var loc_button = $(this);

                if (loc_button.hasClass('btn-default')) {
                    loc_button.toggleClass('btn-default btn-warning');
                    loc_button.button('toggle');
                    loc_button.button('mapclick');

                    $APP.trigger('button.new_locality.activate');
                } else if (loc_button.hasClass('btn-warning')) {
                    loc_button.toggleClass('btn-default btn-warning');
                    loc_button.button('toggle');
                    loc_button.button('reset');

                    $APP.trigger('button.new_locality.deactivate');
                } else {
                    $APP.trigger('button.new_locality.save');
                }
            });

            $('#site-social-icon-open').on('click', function (evt) {
                $('#site-social').animate({width: '115px'}, 500);
            });
            $('#site-social-icon-close').on('click', function (evt) {
                $('#site-social').animate({width: '24px'}, 100);
            });
        }
    }

    // return module
    return module;
}());
