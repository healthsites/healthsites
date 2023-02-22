define([
    'backbone',
    'jquery'
], function (Backbone, $) {
    return Backbone.View.extend({
        initialize: function() {
            this._parameters = {};
            var sPageURL = window.location.search.substring(1),
                sURLVariables = sPageURL.split('&'),
                sParameterName,
                i;

            for (i = 0; i < sURLVariables.length; i++) {
                sParameterName = sURLVariables[i].split('=');
                this._parameters[sParameterName[0]] = decodeURIComponent(sParameterName[1]);
            }
        },
        updateURL: function() {
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
        },
        get: function(parameter) {
            if (this._parameters[parameter]) {
                return this._parameters[parameter];
            } else {
                return null
            }
        },
        set: function(parameter, value) {
            if (value) {
                this._parameters[parameter] = value;
            }
            this.updateURL();
        },
        delete: function(parameter) {
            if (this._parameters[parameter]) {
                delete this._parameters[parameter];
            }
            this.updateURL();
        }
    })
});