'use strict';

/* Controllers */

angular.module('tomorrow.controllers', [])
    .controller('FieldList', ['$scope', '$http', function ($scope, $http) {
        $scope.fields = [];
        $scope.predicate = "name";
        $scope.change_predicate = function (name) {
            if ($scope.predicate === name) {
                $scope.predicate = '-' + name;
                return;
            }
            $scope.predicate = name;
        };
        $http.get("/api/fields/NO").success(function (data) {
            $scope.fields = data;
            angular.forEach($scope.fields, function (field) {
                field.load_details = function ($event) {
                    if (!field.loaded) {
                        var $details = $("#details-" + field.id);
                        $.load_field_production(field.name, $details);
                        field.loaded = true;
                        MathJax.Hub.Queue(["Typeset", MathJax.Hub, "details-" + field.id]);
                    }
                    field.show_details = !field.show_details;
                    $($event.target).scrollTop($($event.target).offset().top);
                };
                field.show_details = false;
            });
        });
    }]);