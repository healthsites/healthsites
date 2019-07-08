define([
    'backbone',
    'jquery',
    'scripts/views/cluster',
], function (Backbone, $, Cluster) {
    return Backbone.View.extend({
        initialize: function () {
            // constructor
            this.MAP = L.map('map', {
                maxZoom: mapMaxZoom
            });

            if (this._isCustomViewPort()) {
            } else if (!this._restoreMapContext()) {
                this.MAP.setView([0, 0], 2);
            }

            this.osm = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
            });
            this.aerial_map = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
                attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
            });
            this.MAP.addLayer(this.osm);

            this.redIcon = L.icon({
                iconUrl: '/static/img/healthsite-marker-red.png',
                iconRetinaUrl: '/static/img/healthsite-marker-red-2x.png',
                iconSize: [35, 43],
                iconAnchor: [17, 43]
            });

            this.addIcon = L.icon({
                iconUrl: '/static/img/add-marker.png',
                iconRetinaUrl: '/static/img/add-marker.png',
                iconSize: [120, 120],
                iconAnchor: [60, 83]
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
                } else {
                    name = "See " + name + " ";
                }
                var nowURL = hasher.getURL().replace("#", "%23");
                javascript:window.open('https://twitter.com/intent/tweet?text=' + name + nowURL, 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=600,width=600');
            });

            // making control for sateloite/osm
            var that = this;
            L.Control.Command = L.Control.extend({
                options: {
                    position: 'bottomleft',
                },
                onAdd: function (map) {
                    var controlDiv = L.DomUtil.create('div', 'leaflet-control-basemap leaflet-bar');
                    var that = this;

                    var basemapControl = L.DomUtil.create('a', "leaflet-control-basemap-child aerial-control", controlDiv);
                    basemapControl.title = 'Satellite View';
                    L.DomEvent
                        .addListener(basemapControl, 'click', L.DomEvent.stopPropagation)
                        .addListener(basemapControl, 'click', L.DomEvent.preventDefault)
                        .addListener(basemapControl, 'click', function () {
                            that.buttonClicked();
                        });
                    this.basemapControl = basemapControl;
                    return controlDiv;
                },
                buttonClicked: function () {
                    if ($(this.basemapControl).hasClass("aerial-control")) {
                        that.MAP.removeLayer(that.osm);
                        that.MAP.addLayer(that.aerial_map);
                        $(this.basemapControl).removeClass("aerial-control");
                        $(this.basemapControl).addClass("osm-control");
                        this.basemapControl.title = 'OSM View';
                    } else {
                        that.MAP.addLayer(that.osm);
                        that.MAP.removeLayer(that.aerial_map);
                        $(this.basemapControl).addClass("aerial-control");
                        $(this.basemapControl).removeClass("osm-control");
                        this.basemapControl.title = 'Satellite View';
                    }
                }
            });
            this.control = new L.Control.Command();
            this.MAP.addControl(this.control);
        },
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

            shared.dispatcher.on('locality.coordinate-changed', function (payload) {
                if (!isNaN(parseInt(payload.geom[0])) && !isNaN(parseInt(payload.geom[1]))) {
                    self.pointLayer.setLatLng([payload.geom[1], payload.geom[0]]);
                    self.MAP.panTo([payload.geom[1], payload.geom[0]]);
                }
            });

            shared.dispatcher.on('locality.create', function (payload) {
                var geom = self.MAP.getCenter();
                shared.dispatcher.trigger('form:update-coordinates', {'latlng': geom});
                self.pointLayer.setLatLng(geom);
                self.MAP.addLayer(self.pointLayer);
                self.MAP.panTo(geom);
            });

            shared.dispatcher.on('locality.edit', function (payload) {
                self.pointLayer.setLatLng(self.original_marker_position);
                self.MAP.addLayer(self.pointLayer);
                self.MAP.panTo(self.original_marker_position);

            });

            shared.dispatcher.on('locality.cancel', function () {
                // user clicked cancel while updating Locality
                self.MAP.removeLayer(self.pointLayer);
                self.pointLayer.setLatLng([0, 0]);
            });

            shared.dispatcher.on('locality.save', function () {
                // user clicked save while updating Locality
                self.MAP.removeLayer(self.pointLayer);
                self.pointLayer.setLatLng([0, 0]);
            });

            shared.dispatcher.on('locality.history-show', function (payload) {
                self.MAP.addLayer(self.historyLayer);
                self.historyLayer.setLatLng([payload.geom[1], payload.geom[0]]);
            });

            shared.dispatcher.on('locality.history-hide', function (payload) {
                self.MAP.removeLayer(self.historyLayer);
                self.historyLayer.setLatLng([0, 0]);
            });


            shared.dispatcher.on('locality.info', function (payload) {
                // remove edit marker if it exists
                if (self.pointLayer) {
                    self.MAP.removeLayer(self.pointLayer);
                    self.pointLayer.setLatLng([0, 0]);
                }

                self.original_marker_position = [payload.geom[1], payload.geom[0]];
                // move map to the marker
                if (payload.zoomto) {
                    self.MAP.setView(self.original_marker_position, self.MAP.getMaxZoom() - 2);
                } else {
                    self.MAP.panTo(self.original_marker_position);
                }
            });

            shared.dispatcher.on('map.update-geoname', function (payload) {
                self._updateGeoname(payload.geoname);
            });

            shared.dispatcher.on('map.update-tag', function (payload) {
                self._updateTag(payload.tag);
                self.clusterLayer.isInit = true;
                self.clusterLayer.usingLines = true;
            });

            shared.dispatcher.on('map.map.update-spec', function (payload) {
                self._updateSpec(payload.spec);
                self.clusterLayer.isInit = true;
                self.clusterLayer.usingLines = true;
            });

            shared.dispatcher.on('map.update-bound', function (payload) {
                self._setFitBound(payload.southwest_lat, payload.southwest_lng, payload.northeast_lat, payload.northeast_lng);
            });

            shared.dispatcher.on('map.create-polygon', function (payload) {
                self._createPolygon(payload.polygon);
            });

            shared.dispatcher.on('map.create-locality-polygon', function (coordinates) {
                self._createPolygonLocality(coordinates);
            });

            shared.dispatcher.on('map.pan', function (payload) {
                self._moveTo(payload.location, payload.zoom);
            });

            shared.dispatcher.on('map.rerender', function (payload) {
                self.MAP.invalidateSize();
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
                'icon': this.addIcon,
                zIndexOffset: 99999999
            });

            this.pointLayer.on('dragend', function (evt) {
                shared.dispatcher.trigger('form:update-coordinates', {'latlng': evt.target._latlng});
            });

            this.historyLayer = L.marker([0, 0], {
                'icon': this.redIcon
            });
        },
        _setupClusterLayer: function () {
            var self = this;
            this.clusterLayer = new Cluster({
                'url': '/api/v2/facilities/cluster'
            });
            self.MAP.addLayer(this.clusterLayer);
        },
        _updateGeoname: function (geoname) {
            this.clusterLayer.clickedPoint_uuid = null;
            this.clusterLayer.clickedPoint_name = null;
            this.clusterLayer.updateGeoname(geoname);
            this.clusterLayer.update();
        },
        _updateTag: function (tag) {
            this.clusterLayer.clickedPoint_uuid = null;
            this.clusterLayer.clickedPoint_name = null;
            this.MAP.setZoom(this.MAP.getMaxZoom());
            this.clusterLayer.updateTag(tag);
            this.clusterLayer.update();
        },
        _updateSpec: function (spec) {
            this.clusterLayer.clickedPoint_uuid = null;
            this.clusterLayer.clickedPoint_name = null;
            this.MAP.setZoom(this.MAP.getMaxZoom());
            this.clusterLayer.updateSpec(spec);
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
                }
            };
            this.geoJson = new L.GeoJSON(mp, {
                style: function (feature) {
                    return styles['area-polygon'];
                }
            }).addTo(this.MAP);
            this.MAP.fitBounds(this.geoJson.getBounds());
        },
        _createPolygonLocality: function (geojsonFeature) {
            if (this.localityPolygon) {
                this.localityPolygon.clearLayers();
            } else {
                this.localityPolygon = new L.GeoJSON([], {
                    style: function (feature) {
                        return styles['locality-polygon'];
                    }
                }).addTo(this.MAP);
            }
            if (geojsonFeature.type !== "Point") {
                this.localityPolygon.addData(geojsonFeature);
            }
        },
        _moveTo: function (location, zoom) {
            if (!zoom) {
                this.MAP.setView(new L.LatLng(location[0], location[1]), this.MAP.getMaxZoom() - 2);
            } else {
                this.MAP.setView(new L.LatLng(location[0], location[1]), zoom);
            }
        }
    })
});