(function ($) {
    'use strict';

    angular.module('tomorrow.directives', []).
        directive('caret', [function () {
            return function (scope, element, attrs) {
                var $this = $(element);
                $this.click(function () {
                    var otherChildren = $($.grep($this.parent().children(), function (child) {
                        return child !== $this[0];
                    }));
                    otherChildren.removeClass("caret-up").removeClass("caret-down");
                    if (!$this.hasClass("caret-up") && !$this.hasClass("caret-down")) {
                        $this.addClass("caret-down");
                        return;
                    }
                    $this.toggleClass("caret-up");
                    $this.toggleClass("caret-down");
                });
            };
        }]).
        directive('information', [function () {
            return function (scope, element, attrs) {
                var $this = $(element),
                    example = $("<div class='information'>Information" +
                        "<span class='fa fa-caret-down'></span>" +
                        "<span class='fa fa-caret-up'></span></div>");
                $this.before(example);
                $this.addClass("information-content");
                example.click(function (event) {
                    $this.toggleClass("open");
                    example.toggleClass("open");
                    event.stopPropagation();
                });
            };
        }]);

}(window.jQuery));