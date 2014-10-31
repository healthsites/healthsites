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
            })
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
        }
    }

    // return module
    return module;
}());