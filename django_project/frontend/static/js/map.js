window.MAP = (function () {
    "use strict";
    // private variables and functions

    // constructor
    var module = function () {
        // create a map in the "map" div, set the view to a given place and zoom
        this.MAP = L.map('map').setView([0, 0], 3);

        // add an OpenStreetMap tile layer
        var hdm = L.tileLayer('http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(this.MAP);

        var osm = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        });

        var baseLayers = {
            "Humanitarian Style": hdm,
            "OpenStreetMap": osm
        };

        // enable Layer control
        L.control.layers(baseLayers).addTo(this.MAP);

        this.MAP.attributionControl.setPrefix(''); // Don't show the 'Powered by Leaflet' text.

        // add markers layer
        this._setupMakersLayer();

        // add point layer
        this._setupPointLayer();


        //bind external events
        this._bindExternalEvents();
    };

    // prototype
    module.prototype = {
        constructor: module,
        _bindExternalEvents:function () {
            var self = this;

            $APP.on('map.show.point', function (evt, payload) {
                self.original_marker_position = [payload.geom[1], payload.geom[0]];

                self.pointLayer.setLatLng(self.original_marker_position);
                self.MAP.addLayer(self.pointLayer);
            });

            $APP.on('map.cancel.edit', function (evt) {
                // user clicked cancel while updating Locality
                self.pointLayer.setLatLng(self.original_marker_position);
            });

            $APP.on('map.remove.point', function (evt) {
                self.MAP.removeLayer(self.pointLayer);
                self.pointLayer.setLatLng([0,0]);
            });
        },

        _setupPointLayer: function () {
            this.pointLayer = L.marker([0, 0], {
                'clickable': true,
                'draggable': true
            });

            this.pointLayer.on('dragend', function (evt) {
                $APP.trigger('locality.map.move', {'latlng': evt.target._latlng});
            });
        },

        _setupMakersLayer: function () {
            var self = this;
            var style = {
                "clickable": true,
                "color": "#00D",
                "weight": 5.0,
                "opacity": 0.3
            };
            var hoverStyle = {
                "weight": 10.0,
                "color": "#0DD",
                "opacity": 0.3
            };

            var geojsonSingleURL = '/localities.json';
            // read localities data
            $.getJSON(geojsonSingleURL, function (data) {
                var localitiesLayer = L.layerGroup();

                for (var i = data.length - 1; i >= 0; i--) {
                    var feature = new L.circleMarker([
                            parseFloat(data[i]['g'][1]),
                            parseFloat(data[i]['g'][0])
                        ], style);
                    feature.id = data[i]['i'];

                    feature.on('mouseover', function (event) {
                        event.target.setStyle(hoverStyle);
                    });
                    feature.on('click', function (event) {
                        $APP.trigger('locality.map.click', {'locality_id': event.target.id});
                    });
                    feature.on('mouseout', function (event) {
                        event.target.setStyle(style);
                    });
                    localitiesLayer.addLayer(feature);
                };

                var markers = new L.MarkerClusterGroup();
                markers.addLayer(localitiesLayer);
                // add markers layer to the map
                self.MAP.addLayer(markers);
            }
        )
    }
}

    // return module
    return module;
}());