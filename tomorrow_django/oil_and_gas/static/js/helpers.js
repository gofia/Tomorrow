/**
 * Created by Lucas-Fievet on 10/19/13.
 */

(function ($) {

    $.number_month = function (date_string) {
        var startYear = parseInt(date_string.substring(0, 4), 10),
            startMonth = parseInt(date_string.substring(5, 7), 10);
        return startYear * 12 + startMonth;
    };

}(window.jQuery));