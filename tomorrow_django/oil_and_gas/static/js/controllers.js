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
                };
                field.open_details = function ($event) {
                    field.show_details = !field.show_details;
                    $($event.target).scrollTop($($event.target).offset().top);
                    field.load_details($event);
                };
                field.show_details = false;
                field.process_interval = undefined;
                field.process_start_year = 0;
                field.process_start_month = 0;
                field.error_avg = Math.round(field.error_avg * 100);
                field.error_std = Math.round(field.error_std * 100);
                field.process = function ($event) {
                    if (field.process_interval !== undefined) {
                        return;
                    }
                    $http.post("/api/fields/process", {
                        field_id: field.id,
                        start_year: field.process_start_year,
                        start_month: field.process_start_month
                    }).success(function (data) {
                        field.process_interval = window.setInterval(function () {
                            $http.post("/api/fields/process/status", {job_id: data.job_id})
                                .success(function (data) {
                                    if (data.status === "PENDING") {
                                        return;
                                    }
                                    if ($.isNumeric(data.status.percent)) {
                                        $($event.target).text(data.status.percent);
                                        return;
                                    }
                                    window.clearInterval(field.process_interval);
                                    field.process_interval = undefined;
                                    field.loaded = false;
                                    field.load_details($event);
                                })
                                .error(function () {
                                    window.clearInterval(field.process_interval);
                                    field.process_interval = undefined;
                                });
                        }, 500);
                    });
                    $event.stopPropagation();
                };
                field.status = function (status) {
                    $http.post("/api/fields/status", {id: field.id, stable: status})
                        .success(function () {
                            field.stable = status;
                        });
                };
            });
        });
        $scope.fields_predicate = "-current_production_oil";
        $scope.change_predicate = function (name) {
            if ($scope.fields_predicate === name) {
                $scope.fields_predicate = '-' + name;
                return;
            }
            $scope.fields_predicate = name;
        };
    }]);