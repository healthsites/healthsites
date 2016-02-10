window.MAP = (function () {
    "use strict";
    // private variables and functions
    var clusterLayer;
    // constructor
    var module = function () {
        // create a map in the "map" div, set the view to a given place and zoom
        this.MAP = L.map('map');

        if (this._isCustomViewPort()) {
        } else if (!this._restoreMapContext()) {
            this.MAP.setView([0, 0], 2);
        }

        var osm = L.tileLayer('http://otile{s}.mqcdn.com/tiles/1.0.0/{type}/{z}/{x}/{y}.{ext}', {
            type: 'map',
            ext: 'jpg',
            attribution: 'Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> &mdash; Map data &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
            subdomains: '1234'
        });
        this.MAP.addLayer(osm);

        this.redIcon = L.icon({
            iconUrl: '/static/img/healthsite-marker-red.png',
            iconRetinaUrl: '/static/img/healthsite-marker-red-2x.png',
            iconSize: [35, 43],
            iconAnchor: [17, 43]
        });

        this.MAP.attributionControl.setPrefix(''); // Don't show the 'Powered by Leaflet' text.

        // add markers layer
        this._setupClusterLayer();

        // add point layer
        this._setupPointLayer();

        // add newLocalityLayer
        this._setupNewLocalityLayer();

        //bind external events
        this._bindExternalEvents();
        this._bindInternalEvents();

        //store initial map context
        this._updateMapContext();

        // hide zoom control on mobile and tablet7
        $('.leaflet-control-zoom').addClass('hidden-xs');
        $('.leaflet-control-zoom').addClass('hidden-sm');


        // activate share
        $('#twitter_share_map').on('click', function (evt) {
            // twitter share
            var name = $("#locality-name").text();
            if (name == "No Name") {
                name = "";
            }
            else {
                name = "See " + name + " ";
            }
            var nowURL = hasher.getURL().replace("#", "%23");
            javascript:window.open('https://twitter.com/intent/tweet?text=' + name + nowURL, 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=600,width=600');
        });
    }

    // prototype
    module.prototype = {
        constructor: module,

        _isCustomViewPort: function () {
            if (sessionStorage.key('northeast_lat') && sessionStorage.key('northeast_lng') &&
                sessionStorage.key('southwest_lat') && sessionStorage.key('southwest_lng')) {

                var northeast_lat = parseFloat(sessionStorage.getItem('northeast_lat'));
                var northeast_lng = parseFloat(sessionStorage.getItem('northeast_lng'));
                var southwest_lat = parseFloat(sessionStorage.getItem('southwest_lat'));
                var southwest_lng = parseFloat(sessionStorage.getItem('southwest_lng'));

                if (northeast_lat && northeast_lng && southwest_lat && southwest_lng) {
                    this.MAP.fitBounds([
                        [southwest_lat, southwest_lng],
                        [northeast_lat, northeast_lng]
                    ]);
                    // Remove them
                    sessionStorage.removeItem('northeast_lat');
                    sessionStorage.removeItem('northeast_lng');
                    sessionStorage.removeItem('southwest_lat');
                    sessionStorage.removeItem('southwest_lng');
                    return true;
                } else {
                    return false;
                }
            } else {
                return false;
            }
        },

        _restoreMapContext: function () {
        },

        _updateMapContext: function () {
            var center = this.MAP.getCenter();
            var zoom = this.MAP.getZoom();

            sessionStorage.setItem('map_center', center.lat + '|' + center.lng);
            sessionStorage.setItem('map_zoom', zoom);
        },

        _bindInternalEvents: function () {
            var self = this;
            this.MAP.on('moveend', function (evt) {
                self._updateMapContext();
            }, this);
        },

        _bindExternalEvents: function () {
            var self = this;

            $APP.on('locality.coordinate-changed', function (evt, payload) {
                if (!isNaN(parseInt(payload.geom[0])) && !isNaN(parseInt(payload.geom[1]))) {
                    self.pointLayer.setLatLng([payload.geom[1], payload.geom[0]]);
                    self.MAP.panTo([payload.geom[1], payload.geom[0]]);
                }
            });

            $APP.on('locality.create', function (evt, payload) {
                var geom = self.MAP.getCenter();
                $APP.trigger('locality.map.move', {'latlng': geom});
                self.pointLayer.setLatLng(geom);
                self.MAP.addLayer(self.pointLayer);
                self.MAP.panTo(geom);
            });

            $APP.on('locality.edit', function (evt, payload) {
                self.pointLayer.setLatLng(self.original_marker_position);
                self.MAP.addLayer(self.pointLayer);
                self.MAP.panTo(self.original_marker_position);

            });

            $APP.on('locality.cancel', function (evt) {
                // user clicked cancel while updating Locality
                self.MAP.removeLayer(self.pointLayer);
                self.pointLayer.setLatLng([0, 0]);
            });

            $APP.on('locality.save', function (evt) {
                // user clicked save while updating Locality
                self.MAP.removeLayer(self.pointLayer);
                self.pointLayer.setLatLng([0, 0]);
            });

            $APP.on('locality.history-show', function (evt, payload) {
                self.historyLayer.setLatLng([payload.geom[1], payload.geom[0]]);
                self.MAP.addLayer(self.historyLayer);
                self.MAP.panTo(payload.geom);
            });

            $APP.on('locality.history-hide', function (evt, payload) {
                self.MAP.removeLayer(self.historyLayer);
                self.historyLayer.setLatLng([0, 0]);
            });


            $APP.on('locality.info', function (evt, payload) {
                // remove edit marker if it exists
                if (self.pointLayer) {
                    self.MAP.removeLayer(self.pointLayer);
                    self.pointLayer.setLatLng([0, 0]);
                }
                ;

                self.original_marker_position = [payload.geom[1], payload.geom[0]];
                // move map to the marker
                if (payload.zoomto) {
                    self.MAP.setView(self.original_marker_position, self.MAP.getMaxZoom() - 2);
                } else {
                    self.MAP.panTo(self.original_marker_position);
                }
            });

            $APP.on('map.update-tag', function (evt, payload) {
                self._updateTag(payload.tag);
            });

            $APP.on('map.update-geoname', function (evt, payload) {
                self._updateGeoname(payload.geoname);
            });

            $APP.on('map.update-bound', function (evt, payload) {
                self._setFitBound(payload.southwest_lat, payload.southwest_lng, payload.northeast_lat, payload.northeast_lng);
            });

            $APP.on('map.create-polygon', function (evt, payload) {
                self._createPolygon(payload.polygon);
            });

            $APP.on('map.pan', function (evt, payload) {
                self._moveTo(payload.location);
            });
        },

        _setupNewLocalityLayer: function () {
            this.newLocalityLayer = L.featureGroup();

            this.drawControl = new L.Control.Draw({
                draw: {
                    polyline: false,
                    polygon: false,
                    rectangle: false,
                    circle: false,
                    marker: {
                        icon: this.redIcon
                    }
                },
                edit: {
                    featureGroup: this.newLocalityLayer
                }
            });
            // create markerDraw control
            this.markerDrawControl = new L.Draw.Marker(this.MAP, this.drawControl.options.draw.marker);
        },

        _setupPointLayer: function () {
            this.pointLayer = L.marker([0, 0], {
                'clickable': true,
                'draggable': true,
                'icon': this.redIcon
            });

            this.pointLayer.on('dragend', function (evt) {
                $APP.trigger('locality.map.move', {'latlng': evt.target._latlng});
            });

            this.historyLayer = L.marker([0, 0], {
                'icon': this.redIcon
            });
        },

        _setupClusterLayer: function () {
            var self = this;
            this.clusterLayer = L.clusterLayer({
                'url': '/localities.json'
            });
            self.MAP.addLayer(this.clusterLayer);
        },

        _updateGeoname: function (geoname) {
            this.clusterLayer.updateGeoname(geoname);
            this.clusterLayer.update();
        },

        _updateTag: function (tag) {
            this.clusterLayer.updateTag(tag);
            this.clusterLayer.update();
        },

        _setFitBound: function (southwest_lat, southwest_lng, northeast_lat, northeast_lng) {
            this.MAP.fitBounds([
                [southwest_lat, southwest_lng],
                [northeast_lat, northeast_lng]
            ]);
        },

        _createPolygon: function (polygon) {
            if (typeof this.geoJson !== "undefined") {
                this.MAP.removeLayer(this.geoJson);
            }
            var mp = {
                "type": "Feature",
                "geometry": {
                    "type": "MultiPolygon",
                    "coordinates": polygon
                },
                "properties": {
                    "name": "MultiPolygon",
                    "style": {
                        color: "blue",
                        opacity: 0.4,
                        fillColor: "blue",
                        fillOpacity: 0.2
                    }
                }
            };
            this.geoJson = new L.GeoJSON(mp, {
                style: function (feature) {
                    return feature.properties.style
                }
            }).addTo(this.MAP);
            this.MAP.fitBounds(this.geoJson.getBounds());
        },

        _moveTo: function (location) {
            this.MAP.setView(new L.LatLng(location[0], location[1]), this.MAP.getMaxZoom() - 2);
        },
    }

    // return module
    return module;
}());
