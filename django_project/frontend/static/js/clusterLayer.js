
(function() {

L.ClusterLayer = L.LayerGroup.extend({

    includes: L.Mixin.Events,

    options: {
        url: ''
    },

    initialize: function(options) {
        L.LayerGroup.prototype.initialize.call(this, []);

        L.Util.setOptions(this, options);

        this._curReq = null;
        this._center = null;
        this._maxBounds = null;

    },

    onAdd: function(map) {

        L.LayerGroup.prototype.onAdd.call(this, map);

        this._center = map.getCenter();
        this._maxBounds = map.getBounds();

        map.on('moveend', this._onMove, this);

        this.update();
    },

    onRemove: function(map) {

        map.off('moveend', this._onMove, this);

        L.LayerGroup.prototype.onRemove.call(this, map);

        for (var i in this._layers) {
            if (this._layers.hasOwnProperty(i)) {
                L.FeatureGroup.prototype.removeLayer.call(this, this._layers[i]);
            }
        }
    },

    update: function() {
        var self = this;
        var bb = this._map.getBounds();


        if(this._curReq && this._curReq.abort)
            this._curReq.abort();       //prevent parallel requests

        var url = this.options.url + L.Util.getParamString({
            'bbox': bb.toBBoxString(),
            'zoom': this._map.getZoom(),
            'iconsize': [48, 46]
        });

        this._curReq = this.getAjax(url, function(response) {
            // clear previous layers
            L.LayerGroup.prototype.clearLayers.call(self);

            this._curReq = null;

            for (var i = response.length - 1; i >= 0; i--) {
                var data = response[i];

                var latlng = L.latLng(data['geom'][1], data['geom'][0]);

                // check if a marker is a cluster marker
                if (data['count'] > 1) {
                    var myIcon = L.divIcon({
                        className: 'marker-icon',
                        html: data['count'],
                        iconAnchor: [24, 23],
                        iconSize: [48, 46]
                    });
                } else {
                    var myIcon = L.icon({
                        iconUrl: '/static/img/healthsite-marker.png',
                        iconRetinaUrl: '/static/img/healthsite-marker-2x.png',
                        iconSize: [26, 46],
                        iconAnchor: [13, 46]
                    });
                }
                var mrk = new L.Marker(latlng, {icon: myIcon});
                mrk.data = {
                    'id': data['id'],
                    'bbox': data['bbox'],
                    'count': data['count']
                }

                mrk.on('click', function (evt) {
                    if (evt.target.data['count'] === 1) {
                        $APP.trigger('locality.map.click', {'locality_id': evt.target.data['id']});
                    }
                    else {
                        var bounds = L.latLngBounds(
                            L.latLng(evt.target.data['bbox'][1], evt.target.data['bbox'][2]),
                            L.latLng(evt.target.data['bbox'][3], evt.target.data['bbox'][0])
                        );
                        // zoom to cluster bounds
                        self._map.fitBounds(bounds);
                    }
                });
                // add marker to the layer
                L.LayerGroup.prototype.addLayer.call(self, mrk);
            }
        });

    },

    _onMove: function(e) {
        this.update();
    },

    getAjax: function(url, cb) {    //default ajax request

        if (window.XMLHttpRequest === undefined) {
            window.XMLHttpRequest = function() {
                try {
                    return new ActiveXObject("Microsoft.XMLHTTP.6.0");
                }
                catch  (e1) {
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
        request.onreadystatechange = function() {
            var response = {};
            if (request.readyState === 4 && request.status === 200) {
                try {
                    if(window.JSON) {
                        response = JSON.parse(request.responseText);
                    } else {
                        response = eval("("+ request.responseText + ")");
                    }
                } catch(err) {
                    console.info(err);
                    response = {};
                }
                cb(response);
            }
        };
        request.send();
        return request;
    }
});

L.clusterLayer = function (options) {
    return new L.ClusterLayer(options);
};

}).call(this);

