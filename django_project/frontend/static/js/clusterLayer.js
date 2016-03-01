(function () {

    L.ClusterLayer = L.LayerGroup.extend({

        includes: L.Mixin.Events,
        options: {
            url: ''
        },

        initialize: function (options) {
            L.LayerGroup.prototype.initialize.call(this, []);

            L.Util.setOptions(this, options);

            this._curReq = null;
            this._center = null;
            this._maxBounds = null;
            this.editMode = false;
            this.localitySaved = false;
            this.clickedPoint_id = false;

            this._bindExternalEvents();
        },

        onAdd: function (map) {

            L.LayerGroup.prototype.onAdd.call(this, map);

            this._center = map.getCenter();
            this._maxBounds = map.getBounds();

            map.on('moveend', this._onMove, this);

            this.update();
        },

        onRemove: function (map) {

            map.off('moveend', this._onMove, this);

            L.LayerGroup.prototype.onRemove.call(this, map);

            for (var i in this._layers) {
                if (this._layers.hasOwnProperty(i)) {
                    L.FeatureGroup.prototype.removeLayer.call(this, this._layers[i]);
                }
            }
        },

        _bindExternalEvents: function () {
            var self = this;

            $APP.on('locality.info', function (evt, payload) {
                self.editMode = false;
                self.clickedPoint_uuid = payload.locality_uuid;
                self.geom = payload.geom;
                self.update(true);
            });

            $APP.on('locality.edit', function (evt) {
                self.editMode = true;
                self.localitySaved = false;
                self.update(true);
            });

            $APP.on('locality.cancel', function (evt) {
                self.editMode = false;
                self.localitySaved = false;
                self.update(true);
            });

            $APP.on('locality.save', function (evt) {
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
            // clear previous layers
            L.LayerGroup.prototype.clearLayers.call(this);

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
                                    iconAnchor: [17, 43]
                                });
                            } else {
                                var myIcon = L.icon({
                                    iconUrl: '/static/img/healthsite-marker.png',
                                    iconRetinaUrl: '/static/img/healthsite-marker-2x.png',
                                    iconSize: [35, 43],
                                    iconAnchor: [17, 43]
                                });
                            }
                        }
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
                    });
                }
                this.render_marker(latlng, centerIcon, [{uuid: self.clickedPoint_uuid}], true);
            }
        },

        render_marker: function (latlng, myIcon, data, isTop) {
            var mrk = new L.Marker(latlng, {icon: myIcon});
            if (isTop) {
                mrk = new L.Marker(latlng, {icon: myIcon, zIndexOffset: 9999999});
            }
            mrk.data = {
                'uuid': data['uuid'],
                'bbox': data['minbbox'],
                'count': data['count'],
            }

            var that = this;
            mrk.on('click', function (evt) {
                if (evt.target.data['count'] === 1) {
                    $APP.trigger('locality.map.click', {'locality_uuid': evt.target.data['uuid']});
                    $APP.trigger('set.hash.silent', {'locality': evt.target.data['uuid']});
                    if (typeof that.geoname != undefined) {
                        window.location.href = "/map#!/locality/" + evt.target.data['uuid'];
                    }
                }
                else {
                    var bounds = L.latLngBounds(
                        L.latLng(evt.target.data['bbox'][1], evt.target.data['bbox'][2]),
                        L.latLng(evt.target.data['bbox'][3], evt.target.data['bbox'][0])
                    );
                    // zoom to cluster bounds
                    this._map.fitBounds(bounds);
                }
            });
            // add marker to the layer
            L.LayerGroup.prototype.addLayer.call(this, mrk);

        },

        update: function (use_cache) {
            var self = this;

            if (this.localitySaved) {
                // skip next map update, probably triggered by panTo... see 'locality.save' event handling
                this.localitySaved = false;
                return;
            }
            var bb = this._map.getBounds();

            if (this._curReq && this._curReq.abort)
                this._curReq.abort();       //prevent parallel requests
            var spec = "";
            var data = "";
            var uuid = "";
            if (this.spec) {
                spec = this.spec['spec'];
                data = this.spec['data'];
                if (this.spec['uuid'] && this.spec['uuid'] != "None") {
                    uuid = this.spec['uuid'];
                }
            }
            var url = this.options.url + L.Util.getParamString({
                    'bbox': bb.toBBoxString(),
                    'zoom': this._map.getZoom(),
                    'iconsize': [48, 46],
                    'geoname': this.geoname,
                    'tag': this.tag,
                    'spec': spec,
                    'data': data,
                    'uuid': uuid,
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
                    }
                    catch (e1) {
                        try {
                            return new ActiveXObject("Microsoft.XMLHTTP.3.0");
                        }
                        catch (e2) {
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
        }
    });

    L.clusterLayer = function (options) {
        return new L.ClusterLayer(options);
    };

}).call(this);

