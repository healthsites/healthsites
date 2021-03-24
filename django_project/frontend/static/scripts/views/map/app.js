define([
    'backbone',
    'jquery',
    'leaflet',
], function (Backbone, $, L) {
    return Backbone.View.extend({
        initialize: function () {
            this._initAPPEvents();
            this._bindExternalEvents();
            this._setupRouter();
        },

        _setupRouter: function () {
            //setup crossroads
            crossroads.addRoute('/locality/{osm_type}/{osm_id}', function (osm_type, osm_id) {
                try {
                    shared.dispatcher.trigger('show-locality-detail', osm_type, osm_id);
                } catch (e) {

                }
            });
            crossroads.addRoute('/review/{review_id}', function (review_id) {
                try {
                    shared.dispatcher.trigger('show-locality-review', review_id);
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
        },

        setHashSilently: function (hash) {
            console.log(hash)
            hasher.changed.active = false;  // disable changed signal
            hasher.setHash(hash);  // set hash without dispatching changed signal
            hasher.changed.active = true;  // re-enable signal
        },

        _bindExternalEvents: function () {
            var self = this;
            this.listenTo(shared.dispatcher, 'set.hash.silent', this.setHashSilently);
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
    })
});