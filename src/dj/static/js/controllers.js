'use strict';
/* global angular, $, app, ENTITIES, USERNAME, USERID, build_entity */
function TopCtrl($scope, $cookies, $rootScope, $window, $location,
                 $log, top, $http, ModelUtils, $filter,
                 $anchorScroll) {
    $scope.top = top;

    $scope.DEBUG = DEBUG;
    $scope.userid = USERID;

    var self = this;




    $scope.initialize = function(data) {
        $scope.load();
    };


    $scope.log = function(message) {
        if (DEBUG) $log.log(message);
    };



    $scope.toDate = function(objs, fields) {
        if (!(fields instanceof Array)) {
            fields = [ fields ];
        }
        if (!(objs instanceof Array)) {
            angular.forEach(fields, function(field) {
                if (objs[field]) {
                    objs[field] = new Date(objs[field].split("T")[0]); //  + " 02:00"
                }
            });
            return objs;
        }
        angular.forEach(objs, function(obj) {
            angular.forEach(fields, function(field) {
                if (obj[field]) {
                    obj[field] = new Date(obj[field].split("T")[0]); //  + " 02:00"
                }
            });
        });
        return objs;
    };


    $scope.toDateStr = function(objs, fields) {
        if (!(fields instanceof Array)) {
            fields = [ fields ];
        }
        if (!(objs instanceof Array)) {
            angular.forEach(fields, function(field) {
                if (objs[field]) {
                    objs[field] = $filter("date")(objs[field], "yyyy-MM-dd");
                }
            });
            return objs;
        }
        angular.forEach(objs, function(obj) {
            angular.forEach(fields, function(field) {
                if (obj[field]) {
                    objs[field] = $filter("date")(objs[field], "yyyy-MM-dd");
                }
            });
        });
        return objs;
    };


    $scope.serialize = function(obj, date_fields) {
        date_fields = typeof date_fields !== 'undefined' ? date_fields : [];
        var str = [];
        angular.forEach(obj, function(value, key) {
            if (value != null) {
                for (var i=0;i<date_fields.length;i++) {
                    if (key == date_fields[i]) {
                        value = $filter("date")(value, "dd/MM/yyyy");
                        break;
                    }
                }
                str.push(key + "=" + encodeURIComponent(value));
            }
        });
        return str.join("&");
    };



    $scope.scrollTo = function(id) {
        $location.hash(id);
        $anchorScroll();
        //$window.scroll(0,$window.pageYOffset-50);
    };
}


function CommonCtrl($scope,top, $log, $filter, ModelUtils, ngTableParams) {
    $scope.name = 'common';
    $scope.top = top;
    $scope.paginatedResources = [];
    top[$scope.name+'s'] = []; // anciennement $scope.resources
    top[$scope.name] = {};
    top[$scope.name+'_reload'] = false;
    $scope.errors = {};

    $scope.initialize = function(service_name) {

    };

    $scope.isEmpty = function(obj) {
        return (Object.keys($scope.errors).length==0);
    };

}

