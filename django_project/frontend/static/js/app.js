var APP = (function () {
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
        }).addTo(this.MAP);

        var baseLayers = {
            "Humanitarian Style": hdm,
            "OpenStreetMap": osm
        };

        // enable Layer control
        L.control.layers(baseLayers).addTo(this.MAP);

        this.MAP.attributionControl.setPrefix(''); // Don't show the 'Powered by Leaflet' text.
    };

    // prototype
    module.prototype = {
        constructor: module
    };

    // return module
    return module;
}());