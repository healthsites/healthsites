class Parameters {

    constructor() {
        this._parameters = {};
        var sPageURL = window.location.search.substring(1),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;

        for (i = 0; i < sURLVariables.length; i++) {
            sParameterName = sURLVariables[i].split('=');
            this._parameters[sParameterName[0]] = decodeURIComponent(sParameterName[1]);
        }
    }

    updateURL() {
        var currentUrl = window.location.toString();
        var domains = currentUrl.split('?');
        var hashes = currentUrl.split('#');

        // construct parameters
        var newParameters = [];
        $.each(this._parameters, function (key, value) {
            if (key && value) {
                newParameters.push(key + '=' + value);
            }
        });
        newParameters = newParameters.join('&');

        // join it
        var newURL = domains[0];
        if (newParameters) {
            newURL += '?' + newParameters
        }
        if (hashes[1]) {
            newURL += '#' + hashes[1];
        }
        window.history.pushState({}, document.title, newURL);
    }

    get(parameter) {
        if (this._parameters[parameter]) {
            return this._parameters[parameter];
        } else {
            return null
        }
    }

    set(parameter, value) {
        if (value) {
            this._parameters[parameter] = value;
        }
        this.updateURL();
    }

    delete(parameter) {
        if (this._parameters[parameter]) {
            delete this._parameters[parameter];
        }
        this.updateURL();
    }

}

var parameters = new Parameters();

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
