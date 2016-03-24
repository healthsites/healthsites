/**
 * Created by meomancer on 14/12/15.
 */
var monthNames = [
    "January", "February", "March",
    "April", "May", "June", "July",
    "August", "September", "October",
    "November", "December"
];
function getDateString(date_input) {
    var date = new Date(date_input);
    var day = date.getDate();
    var monthIndex = date.getMonth();
    var year = date.getFullYear();
    var hour = ("0" + date.getHours()).slice(-2);
    var minute = ("0" + date.getMinutes()).slice(-2);
    var second = ("0" + date.getSeconds()).slice(-2);

    return day + ' ' + monthNames[monthIndex] + ' ' + year + ' ' + hour + ':' + minute + ':' + second;
}

// Will remove all false values: undefined, null, 0, false, NaN and "" (empty string)
function cleanArray(actual) {
    var newArray = new Array();
    for (var i = 0; i < actual.length; i++) {
        if (actual[i]) {
            newArray.push(actual[i]);
        }
    }
    return newArray;
}

Array.prototype.getUnique = function () {
    var u = {}, a = [];
    for (var i = 0, l = this.length; i < l; ++i) {
        if (u.hasOwnProperty(this[i])) {
            continue;
        }
        a.push(this[i]);
        u[this[i]] = 1;
    }
    return a;
}

String.prototype.replaceAll = function (search, replacement) {
    var target = this;
    return target.replace(new RegExp(search, 'g'), replacement);
}

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toUTCString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1);
        if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
    }
    return "";
}

function resetCookies() {
    setCookie("type", "", 30);
    setCookie("center", "", 30);
    setCookie("zoom", "", 30);
    setCookie("uuid", "", 30);
    setCookie("oldurl", "", 30);
}