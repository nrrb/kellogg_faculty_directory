'use strict';

/* Controllers */

var kfkApp = angular.module('kfkApp', []);

kfkApp.controller('FacultyListCtrl', function($scope, $http) {
  $http.get('faculty.json').success(function(data) {
    $scope.faculty = data;
  });
  $scope.orderProp = 'name';
});
