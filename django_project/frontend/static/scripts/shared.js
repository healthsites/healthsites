var shared = {};

// extract parameters
var parameters = {};
var sPageURL = window.location.search.substring(1),
    sURLVariables = sPageURL.split('&'),
    sParameterName,
    i;

for (i = 0; i < sURLVariables.length; i++) {
    sParameterName = sURLVariables[i].split('=');
    parameters[sParameterName[0]] = decodeURIComponent(sParameterName[1]);
}

shared['hash'] = function () {
    return window.location.hash.substr(2);
};

shared['currentID'] = function () {
    return shared.hash().replace('/locality/', '')
}

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
