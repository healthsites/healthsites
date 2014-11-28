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

        // init localitySidebar
        new LocalitySidebar();

        this._initAPPEvents();

        this._bindExternalEvents();

        this._setupRouter();
    };

    // prototype
    module.prototype = {
        constructor: module,

        _setupRouter: function() {
            //setup crossroads
            crossroads.addRoute('/locality/{id}', function(id){
                $APP.trigger('locality.map.click', {'locality_id': id, 'zoomto': true});
            });

            //setup hasher
            hasher.prependHash = '!';
            hasher.initialized.add(this._parseHash);
            hasher.changed.add(this._parseHash);
            hasher.init();
        },

        _parseHash: function (newHash, oldHash){
            crossroads.parse(newHash);
        },

        setHashSilently: function (hash){
            hasher.changed.active = false;  // disable changed signal
            hasher.setHash(hash);  // set hash without dispatching changed signal
            hasher.changed.active = true;  // re-enable signal
        },

        _bindExternalEvents: function () {
            var self = this;
            $(window).resize(function() {
                $APP.trigger('locality.show-info-adjust');
            });

            $APP.on('set.hash.silent', function (evt, payload) {
                self.setHashSilently('/locality/' + payload.locality);
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
