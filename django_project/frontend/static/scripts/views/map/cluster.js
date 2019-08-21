define([
    'backbone',
    'jquery'
], function (Backbone, $) {
    return L.FeatureGroup.extend({
        includes: L.Mixin.Events,
        options: {
            url: ''
        },

        initialize: function (options) {
            L.FeatureGroup.prototype.initialize.call(this, []);

            L.Util.setOptions(this, options);

            this._curReq = null;
            this._center = null;
            this._maxBounds = null;
            this.editMode = false;
            this.localitySaved = false;
            this.clickedPoint_id = false;
            this.usingLines = false;
            this.lines = [];

            this._bindExternalEvents();
        },

        onAdd: function (map) {

            L.FeatureGroup.prototype.onAdd.call(this, map);

            this._center = map.getCenter();
            this._maxBounds = map.getBounds();

            map.on('moveend', this._onMove, this);

            this.update();
        },

        onRemove: function (map) {

            map.off('moveend', this._onMove, this);

            L.FeatureGroup.prototype.onRemove.call(this, map);

            for (var i in this._layers) {
                if (this._layers.hasOwnProperty(i)) {
                    L.FeatureGroup.prototype.removeLayer.call(this, this._layers[i]);
                }
            }
        },

        _bindExternalEvents: function () {
            var self = this;

            shared.dispatcher.on('locality.info', function (payload) {
                self.editMode = false;
                self.clickedPoint_uuid = payload.locality_uuid;
                self.clickedPoint_name = payload.locality_name;
                self.geom = payload.geom;
                if (this.usingLines) {
                    self.update(false);
                } else {
                    self.update(true);
                }
            });

            shared.dispatcher.on('locality.edit', function () {
                self.editMode = true;
                self.localitySaved = false;
                self.update(true);
            });

            shared.dispatcher.on('locality.cancel', function () {
                self.editMode = false;
                self.localitySaved = false;
                self.update(true);
            });

            shared.dispatcher.on('locality.save', function () {
                self.editMode = false;
                self.update();
                // as locality was recently saved and the map was updated, we need
                // to suppress first next event, if caused by 'moveend'
                // TODO: we should probably create a custom map event and encapsulate this behaviour
                self.localitySaved = true;
            });
        },


        _render_map: function (response) {
            var self = this;
            var otherMarker = [];
            // clear previous layers
            L.FeatureGroup.prototype.clearLayers.call(this);

            // emptying line array
            for (var i = 0; i < this.lines.length; i++) {
                this._map.removeLayer(this.lines[i]);
            }
            this.lines = [];

            this._curReq = null;
            var centerIcon;
            if (typeof response != 'undefined') {
                for (var i = response.length - 1; i >= 0; i--) {
                    var data = response[i];

                    // check if marker was clicked and remove it
                    var latlng = L.latLng(data['geom'][1], data['geom'][0]);
                    if (this.clickedPoint_uuid && data['uuid'] === this.clickedPoint_uuid) {
                        if (this.editMode) {
                            // skip processing of this point, don't render or add events
                            continue;
                        }
                    } else {
                        // check if a marker is a cluster marker
                        if (data['count'] > 1) {
                            var myIcon = L.divIcon({
                                className: 'marker-icon',
                                html: data['count'],
                                iconAnchor: [24, 59],
                                iconSize: [48, 59]
                            });
                        } else {
                            if (data['uuid'] === this.clickedPoint_uuid) {
                                centerIcon = L.icon({
                                    iconUrl: '/static/img/pin-red.svg',
                                    iconRetinaUrl: '/static/img/pin-red.svg',
                                    iconSize: [35, 43],
                                    iconAnchor: [17, 43],
                                    popupAnchor: [0, -43]
                                });
                            } else {
                                var myIcon = L.icon({
                                    iconUrl: '/static/img/healthsite-marker.png',
                                    iconRetinaUrl: '/static/img/healthsite-marker-2x.png',
                                    iconSize: [35, 43],
                                    iconAnchor: [17, 43],
                                    popupAnchor: [0, -43]
                                });
                            }
                        }
                        otherMarker.push(latlng);
                        this.render_marker(latlng, myIcon, data);
                    }
                }
            }
            if (this.clickedPoint_uuid && !this.editMode) {
                if (!centerIcon) {
                    var latlng = L.latLng(self.geom[1], self.geom[0]);
                    centerIcon = L.icon({
                        iconUrl: '/static/img/pin-red.svg',
                        iconRetinaUrl: '/static/img/pin-red.svg',
                        iconSize: [35, 43],
                        iconAnchor: [17, 43],
                        popupAnchor: [0, -43]
                    });
                }
                this.render_marker(latlng, centerIcon, {
                    count: 1,
                    name: self.clickedPoint_name,
                    uuid: self.clickedPoint_uuid
                }, true);
            } else if (this.clickedPoint_uuid && this.editMode) {
                if (typeof this.focused_marker != "undefined" && this.focused_marker != null) {
                    this._map.removeLayer(this.focused_marker);
                }
                this.focused_marker = null;
            } else if (!this.clickedPoint_uuid || this.clickedPoint_uuid == "") {
                if (typeof this.focused_marker != "undefined" && this.focused_marker != null) {
                    this._map.removeLayer(this.focused_marker);
                }
                this.focused_marker = null;
            }
            if (this.usingLines) {
                if (typeof this.focused_marker != "undefined" && this.focused_marker != null) {
                    for (var i = 0; i < otherMarker.length; i++) {
                        var pointA = new L.latLng(self.geom[1], self.geom[0]);
                        var pointB = otherMarker[i]
                        var pointList = [pointA, pointB];
                        var line = new L.Polyline(pointList, {
                            color: 'red',
                            weight: 2,
                            opacity: 0.5,
                            smoothFactor: 1
                        });
                        this._map.addLayer(line);
                        this.lines.push(line);
                    }
                }
            }

            if (typeof this.isInit != "undefined" && this.isInit) {
                this.isInit = false;
                if (typeof this.focused_marker != "undefined" && this.focused_marker != null) {
                    //create dummy
                    var myIcon = L.icon({
                        iconUrl: '/static/img/healthsite-marker.png',
                        iconRetinaUrl: '/static/img/healthsite-marker-2x.png',
                        iconSize: [35, 43],
                        iconAnchor: [17, 43],
                        popupAnchor: [0, -43]
                    });
                    var dummy_marker = this.render_marker(this.focused_marker.data['latlng'], myIcon, {});
                    this._map.fitBounds(this.getBounds());
                    L.FeatureGroup.prototype.removeLayer.call(this, dummy_marker);
                } else {
                    this._map.fitBounds(this.getBounds());
                }
            }
        },

        render_marker: function (latlng, myIcon, data, isFocused) {
            var mrk = new L.Marker(latlng, {icon: myIcon});
            if (isFocused) {
                mrk = new L.Marker(latlng, {icon: myIcon, zIndexOffset: 9999999});
            }
            mrk.data = {
                'latlng': latlng,
                'uuid': data['uuid'],
                'bbox': data['minbbox'],
                'count': data['count'],
                'name': data['name'],
            }
            var that = this;
            mrk.on('click', function (evt) {
                // event for getting master's uuid
                if ($("#report-popup").is(":visible")) {
                    $("#report-popup-text").val(evt.target.data['uuid']);
                } else {
                    if (evt.target.data['count'] === 1) {
                        if (window.location.href.indexOf("map") > -1) {
                            var identifiers = evt.target.data['uuid'].split('/');
                            shared.dispatcher.trigger(
                                'show-locality-detail', identifiers[0], identifiers[1]
                            );
                            shared.dispatcher.trigger('set.hash.silent', '/locality/' + evt.target.data['uuid']);
                        } else {
                            window.location.href = "/map#!/locality/" + evt.target.data['uuid'];
                        }
                    } else {
                        var bounds = L.latLngBounds(
                            L.latLng(evt.target.data['bbox'][1], evt.target.data['bbox'][2]),
                            L.latLng(evt.target.data['bbox'][3], evt.target.data['bbox'][0])
                        );
                        // zoom to cluster bounds
                        that._map.fitBounds(bounds);
                    }
                }
            });
            // add marker to the layer
            if (!isFocused) {
                L.FeatureGroup.prototype.addLayer.call(this, mrk);
            } else {
                if (typeof this.focused_marker == "undefined" || this.focused_marker == null || this.focused_marker.data['uuid'] != mrk.data['uuid'] || this.focused_marker.data['latlng'].lat != mrk.data['latlng'].lat || this.focused_marker.data['latlng'].lng != mrk.data['latlng'].lng) {
                    if (typeof this.focused_marker != "undefined" && this.focused_marker != null) {
                        this._map.removeLayer(this.focused_marker);
                    }
                    this.focused_marker = mrk;
                    this._map.addLayer(this.focused_marker);
                }
            }

            //show popup is it is focused locality and in viewport
            if (isFocused) {
                var minx = this._map.getBounds()._southWest.lng;
                var miny = this._map.getBounds()._southWest.lat;
                var maxx = this._map.getBounds()._northEast.lng;
                var maxy = this._map.getBounds()._northEast.lat;

                var lng = mrk.getLatLng().lng;
                var lat = mrk.getLatLng().lat;
                if (maxx >= lng && minx <= lng && maxy >= lat && miny <= lat) {
                    mrk.openPopup();
                }
            }
            return mrk;
        },

        update: function (use_cache) {
            var self = this;

            if (this.localitySaved) {
                // skip next map update, probably triggered by panTo... see 'locality.save' event handling
                this.localitySaved = false;
                return;
            }

            if (this._map) {
                var bb = this._map.getBounds();

                if (this._curReq && this._curReq.abort)
                    this._curReq.abort();       //prevent parallel requests
                var geoname = "";
                var tag = "";
                var spec = "";
                var data = "";
                var uuid = "";
                if (this.geoname) {
                    geoname = this.geoname;
                }
                if (this.tag) {
                    tag = this.tag;
                }
                if (this.spec) {
                    spec = this.spec['spec'];
                    data = this.spec['data'];
                    if (this.spec['uuid'] && this.spec['uuid'] != "None") {
                        uuid = this.spec['uuid'];
                    }
                }
                if (this.clickedPoint_uuid) {
                    uuid = this.clickedPoint_uuid;
                }
                var url = this.options.url + L.Util.getParamString({
                    'bbox': bb.toBBoxString(),
                    'zoom': this._map.getZoom(),
                    'iconsize': [48, 46],
                    'geoname': geoname,
                    'tag': tag,
                    'spec': spec,
                    'data': data,
                    'uuid': uuid
                });
                // when using cached data we don't need to make any new requests
                // for example, this is useful when changing app contexts without changing map view
                if (use_cache) {
                    self._render_map(self.ajax_response);
                } else {
                    this._curReq = this.getAjax(url, function (response) {
                        self._render_map(response);
                        // cache response
                        self.ajax_response = response;
                    });
                }
            }
        },

        _onMove: function (e) {
            // simply update the layer
            this.update();
        },

        getAjax: function (url, cb) {    //default ajax request

            if (window.XMLHttpRequest === undefined) {
                window.XMLHttpRequest = function () {
                    try {
                        return new ActiveXObject("Microsoft.XMLHTTP.6.0");
                    } catch (e1) {
                        try {
                            return new ActiveXObject("Microsoft.XMLHTTP.3.0");
                        } catch (e2) {
                            throw new Error("XMLHttpRequest is not supported");
                        }
                    }
                };
            }
            var request = new XMLHttpRequest();
            request.open('GET', url);
            request.onreadystatechange = function () {
                var response = {};
                if (request.readyState === 4 && request.status === 200) {
                    try {
                        if (window.JSON) {
                            response = JSON.parse(request.responseText);
                        } else {
                            response = eval("(" + request.responseText + ")");
                        }
                    } catch (err) {
                        console.info(err);
                        response = {};
                    }
                    cb(response);
                }
            };
            request.send();
            return request;
        },

        updateGeoname: function (geoname) {
            this.geoname = geoname;
        },

        updateTag: function (tag) {
            this.tag = tag;
        },

        updateSpec: function (spec) {
            this.spec = spec;
            if (spec.geom[0] != 0.0 && spec.geom[1] != 0.0) {
                this.clickedPoint_uuid = spec.uuid;
                this.clickedPoint_name = spec.name;
                this.geom = spec.geom;
            }
        }
    });
});