'use strict';

/* Controllers */

angular.module('tomorrow.controllers', [])
    .controller('FieldList', ['$scope', '$http', function ($scope, $http) {
        $scope.countries = [];
        $http.get("/api/countries").success(function (data) {
            $scope.countries = data;
            angular.forEach($scope.countries, function (country) {
                country.load_details = function ($event) {
                    if (!country.loaded) {
                        var $details = $("#country-details-" + country.id);
                        $.plot_details($details)(country);
                        country.loaded = true;
                        MathJax.Hub.Queue(["Typeset", MathJax.Hub, "country-details-" + country.id]);
                    }
                    country.show_details = !country.show_details;
                    $($event.target).scrollTop($($event.target).offset().top);
                };
                country.show_details = false;
            });
        });
        $scope.fields = [];
        $http.get("/api/fields/NO").success(function (data) {
            $scope.fields = data;
            angular.forEach($scope.fields, function (field) {
                field.load_details = function ($event) {
                    if (!field.loaded) {
                        var $details = $("#details-" + field.id);
                        $.load_field_production(field.id, $details);
                        field.loaded = true;
                        MathJax.Hub.Queue(["Typeset", MathJax.Hub, "details-" + field.id]);
                    }
                    field.show_details = !field.show_details;
                    $($event.target).scrollTop($($event.target).offset().top);
                };
                field.show_details = false;
            });
        });
        $scope.predicate = "name";
        $scope.change_predicate = function (name) {
            if ($scope.predicate === name) {
                $scope.predicate = '-' + name;
                return;
            }
            $scope.predicate = name;
        };
    }]);