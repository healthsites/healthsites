var shared = {};
var parameters;
var map;
shared['hash'] = function () {
    return window.location.hash.substr(2);
};

shared['currentID'] = function () {
    return shared.hash().replace('/locality/', '')
};

// Styles
var styles = {
    'locality-polygon': {
        color: "#f44a52",
        opacity: 1,
        weight: 2,
        fillColor: "#f44a52",
        fillOpacity: 0.4
    },
    'area-polygon': {
        color: "#f44a52",
        opacity: 0.2,
        weight: 1,
        fillColor: "#f44a52",
        fillOpacity: 0.2
    }
};
