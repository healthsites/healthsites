var shared = {};
shared['hash'] = function () {
    return window.location.hash.substr(2);
};

shared['currentID'] = function () {
    return shared.hash().replace('/locality/', '')
};

shared['replaceGeonameSearch'] = function (geoname) {
    var currentUrl = window.location.toString();
    if (!geoname) {
        if (parameters['geoname']) {
            currentUrl = currentUrl.replace(
                'geoname=' + parameters['geoname'], '')
        }
    } else {
        if (parameters['geoname']) {
            currentUrl = currentUrl.replace(
                parameters['geoname'], geoname)
        }
    }
    window.history.pushState({}, document.title, currentUrl);
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
