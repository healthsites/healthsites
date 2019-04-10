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