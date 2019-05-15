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
            crossroads.addRoute('/locality/{osm_type}/{osm_id}', function (osm_type, osm_id) {
                console.log(osm_type);
                try {
                    shared.dispatcher.trigger('show-locality-detail', {
                        'osm_type': osm_type, 'osm_id': osm_id
                    });
                } catch (e) {

                }
            });
            //setup hasher
            hasher.prependHash = '!';
            hasher.initialized.add(this._parseHash);
            hasher.changed.add(this._parseHash);
            hasher.init();
        },

        _parseHash: function (newHash, oldHash) {
            crossroads.parse(newHash);
            if (newHash == "") {
                changeToDefault();
            }
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

        getCenterOfMap: function () {
            if (_MAP) {
                return _MAP.MAP.getCenter();
            } else {
                return {lat: 0, lng: 0}
            }
        },

        getZoomOfMap: function () {
            if (_MAP) {
                return _MAP.MAP.getZoom();
            } else {
                return 0
            }
        },

        getNowHasher: function () {
            return hasher.getHash();
        }
    }

    // return module
    return module;
}());
