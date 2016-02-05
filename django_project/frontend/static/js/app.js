if (typeof APP == 'undefined') {
    APP = {};
    $APP = $(APP);
}

window.APP = (function () {
    "use strict";
    // private variables and functions
    var _MAP;
    // constructor
    var module = function () {
        // init map
        _MAP = new MAP();

        // init localitySidebar
        this.$sidebar = new LocalitySidebar();

        this._initAPPEvents();

        this._bindExternalEvents();

        this._setupRouter();
    };

    // prototype
    module.prototype = {
        constructor: module,

        _setupRouter: function () {
            //setup crossroads
            crossroads.addRoute('/locality/{uuid}', function (uuid) {
                $APP.trigger('locality.map.click', {'locality_uuid': uuid, 'zoomto': true});
            });
            //setup crossroads
            crossroads.addRoute('/locality/{uuid}/{changeset}', function (uuid, changeset) {
                $APP.trigger('locality.map.click', {'locality_uuid': uuid, 'zoomto': true, 'changeset': changeset});
            });

            //setup hasher
            hasher.prependHash = '!';
            hasher.initialized.add(this._parseHash);
            hasher.changed.add(this._parseHash);
            hasher.init();
        },

        _parseHash: function (newHash, oldHash) {
            crossroads.parse(newHash);
        },

        setHashSilently: function (hash) {
            hasher.changed.active = false;  // disable changed signal
            hasher.setHash(hash);  // set hash without dispatching changed signal
            hasher.changed.active = true;  // re-enable signal
        },

        _bindExternalEvents: function () {
            var self = this;
            $(window).resize(function () {
                $APP.trigger('locality.show-info-adjust');
            });

            $APP.on('set.hash.silent', function (evt, payload) {
                self.setHashSilently('/locality/' + payload.locality);
            });
        },

        _initAPPEvents: function () {

            $('#site-social-icon-open').on('click', function (evt) {
                if ($(this).hasClass('mdi-social-share')) {
                    $('#site-social').animate({width: '115px'}, 100);
                    $(this).removeClass('mdi-social-share').addClass('mdi-content-clear');
                } else {
                    $('#site-social').animate({width: '24px'}, 100);
                    $(this).removeClass('mdi-content-clear').addClass('mdi-social-share');
                }
            });

            $('.facebook-hs-share').on('click', function (evt) {
                FB.ui({
                    method: 'share',
                    href: 'http://healthsites.io/'
                }, function (response) {
                });
            });
        },

        _openSidebar: function () {
            $('#sidebar').addClass('active');
            $('#sidebar-helper').addClass('active');
        },

        _closeSidebar: function () {

        },
    }

    // return module
    return module;
}());
