var shared = {};
var parameters;
let dataFilters = {};
var map;
shared['hash'] = function () {
    return window.location.hash.substr(2);
};

shared['currentID'] = function () {
    if (shared.hash().indexOf('/locality/') !== -1) {
        return shared.hash().replace('/locality/', '')
    }
    return null;
};

shared['currentReviewID'] = function () {
    if (shared.hash().indexOf('/review/') !== -1) {
        return shared.hash().replace('/review/', '')
    }
    return null;
};
shared['formOrder'] = ['name', 'amenity', 'healthcare', 'health_amenity_type', 'operator'];

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
