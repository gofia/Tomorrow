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

}(window.jQuery));