/**
 * Google Analytics 4 tracking for healthsites.io.
 *
 * The site is a single page app on top of Django templates: the map keeps
 * the selected country and place in the query string (?country=…&place=…)
 * and the open facility in the URL hash (#!/locality/node/123). GA4 drops
 * both the query string and the hash from its "page path" dimension, so
 * without help every visit is reported as "/".
 *
 * This file:
 *   - loads gtag.js with automatic page views disabled,
 *   - sends a virtual page view whose path encodes country, place and
 *     facility, e.g. /map/country/Senegal/locality/node/123,
 *   - re-sends it whenever the hash or history state changes,
 *   - exposes window.hsAnalytics for custom events (downloads, search).
 */
(function (window, document) {
    var MEASUREMENT_ID = 'G-TFPG6WH4CZ';

    window.dataLayer = window.dataLayer || [];
    function gtag() {
        window.dataLayer.push(arguments);
    }
    window.gtag = window.gtag || gtag;

    gtag('js', new Date());
    gtag('config', MEASUREMENT_ID, {send_page_view: false});

    var script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=' + MEASUREMENT_ID;
    document.head.appendChild(script);

    /** Build a path that carries the state GA4 would otherwise discard. */
    function virtualPath() {
        var path = window.location.pathname;
        var query = window.location.search.substring(1).split('&');
        var params = {};
        for (var i = 0; i < query.length; i++) {
            var pair = query[i].split('=');
            if (pair[0]) {
                try {
                    params[pair[0]] = decodeURIComponent(pair[1] || '');
                } catch (e) {
                    params[pair[0]] = pair[1] || '';
                }
            }
        }
        if (params.country) {
            path += '/country/' + params.country;
        }
        if (params.place) {
            path += '/place/' + params.place;
        }
        var hash = window.location.hash.replace(/^#!?/, '');
        if (hash) {
            path += (hash.charAt(0) === '/' ? '' : '/') + hash;
        }
        return path.replace(/\/{2,}/g, '/').replace(/\s+/g, '-');
    }

    var lastPath = null;

    function pageView() {
        var path = virtualPath();
        if (path === lastPath) {
            return;
        }
        lastPath = path;
        gtag('event', 'page_view', {
            page_path: path,
            page_location: window.location.origin + path,
            page_title: document.title
        });
    }

    function event(name, params) {
        gtag('event', name, params || {});
    }

    window.hsAnalytics = {pageView: pageView, event: event};

    // Initial view.
    pageView();

    // Facility opened or closed: hasher changes the hash.
    window.addEventListener('hashchange', pageView);

    // Back and forward buttons.
    window.addEventListener('popstate', pageView);

    // Place search rewrites the query string with pushState.
    ['pushState', 'replaceState'].forEach(function (method) {
        var original = window.history[method];
        if (typeof original !== 'function') {
            return;
        }
        window.history[method] = function () {
            var result = original.apply(this, arguments);
            pageView();
            return result;
        };
    });
})(window, document);
