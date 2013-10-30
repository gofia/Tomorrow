/**
 * Created by Lucas-Fievet on 10/19/13.
 */

(function ($) {

    $.to_date = function (date_string) {
        var start_year = parseInt(date_string.substring(0, 4), 10),
            start_month = parseInt(date_string.substring(5, 7), 10),
            start_day = parseInt(date_string.substring(8, 10), 10);
        return Date.UTC(start_year, start_month, start_day);
    };

    $.month_diff = function (date1, date2) {
        return Math.round((date2 - date1) / (1000 * 3600 * 24 * 30.5));
    };

    $.stretched_exponential = function (A, tau, beta) {
        return function (x) {
            var result = x / Math.abs(tau);
            result = Math.pow(result, beta);
            result *= tau / Math.abs(tau);
            result = Math.exp(result);
            result *= A;
            return result;
        };
    };

}(window.jQuery));