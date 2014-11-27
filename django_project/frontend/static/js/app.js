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

            $(window).resize(function() {
                $APP.trigger('locality.show-info-adjust');
            });
        },

        _initAPPEvents: function () {

            $('#site-social-icon-open').on('click', function (evt) {
                $('#site-social').animate({width: '115px'}, 500);
            });
            $('#site-social-icon-close').on('click', function (evt) {
                $('#site-social').animate({width: '24px'}, 100);
            });
        },

        _openSidebar: function() {
            $('#sidebar').addClass('active');
            $('#sidebar-helper').addClass('active');
        },

        _closeSidebar: function() {

        }
    }

    // return module
    return module;
}());
