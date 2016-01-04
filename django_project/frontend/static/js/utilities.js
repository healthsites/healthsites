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
    console.log(date_input);
    var date = new Date(date_input);
    var day = date.getDate();
    var monthIndex = date.getMonth();
    var year = date.getFullYear();
    var hour = ("0" + date.getHours()).slice(-2);
    var minute = date.getMinutes();
    var second = ("0" + date.getSeconds()).slice(-2);

    return day + ' ' + monthNames[monthIndex] + ' ' + year + ' ' + hour + ':' + minute + ':' + second;
}