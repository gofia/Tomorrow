'use strict';


// Declare app level module which depends on filters, and services
angular.module('tomorrow', [
  'tomorrow.controllers',
  'tomorrow.directives'
])
.config(['$routeProvider', function ($routeProvider) {

}])
.config(['$httpProvider', function ($httpProvider) {
    $httpProvider.defaults.headers.common['X-CSRFToken'] = $.get_cookie("csrftoken");
}]);
