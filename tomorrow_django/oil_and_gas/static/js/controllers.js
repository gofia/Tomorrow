'use strict';

/* Controllers */

angular.module('tomorrow.controllers', [])
    .controller('FieldList', ['$scope', '$http', function ($scope, $http) {
        $scope.countries = [];
        $http.get("/api/countries").success(function (data) {
            $scope.countries = data;
            angular.forEach($scope.countries, function (country) {
                country.load_details = function ($event) {
                    country.show_details = !country.show_details;
                    if (!country.loaded) {
                        var $details = $("#country-details-" + country.id);
                        $.plot_details($details)(country);
                        country.loaded = true;
                        MathJax.Hub.Queue(["Typeset", MathJax.Hub, "country-details-" + country.id]);
                    }
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
                field.process = function () {
                    $http.post("/api/fields/process", { field_id: field.id }, function (data) {
                        var test;
                        $http.post("/api/fields/process/status", { job_id: data.job_id });
                    });
                };
            });
        });
        $scope.fields_predicate = "name";
        $scope.change_predicate = function (name) {
            if ($scope.fields_predicate === name) {
                $scope.fields_predicate = '-' + name;
                return;
            }
            $scope.fields_predicate = name;
        };
    }]);