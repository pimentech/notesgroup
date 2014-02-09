'use strict';
/* global angular, $, app, DEBUG, USERNAME, USERID, CARTE */

var modules = ['ngCookies'];

var app = angular.module('myApp', modules);
var ENTITIES = [];

app.config(['$compileProvider', function($compileProvider){
    // pour xport csv
    if (angular.isDefined($compileProvider.urlSanitizationWhitelist)) {
        $compileProvider.urlSanitizationWhitelist(
                /^\s*(https?|ftp|mailto|file|data):/);
    } else {
        $compileProvider.aHrefSanitizationWhitelist(
                /^\s*(https?|ftp|mailto|file|data):/);
    }
}]);


app.run(function($rootScope, $log, $http, $cookies) {
    $http.defaults.headers.common['X-CSRFToken'] = $cookies['csrftoken'];


    $rootScope.jsonPrint = function(obj) {
        var printed;
        if (obj instanceof Array) {
            printed = '<ul>';
            for (var i=0;i<obj.length;i++) {
                printed += '<li>'
                    + $rootScope.jsonPrint(obj[i])
                    + '</li>';
            }
            printed += '</ul>';
        }
        else if (obj instanceof Object) {
            printed = '<dl>';
            for (var key in obj) {
                printed += '<dt>' + key + '</dt>'
                    + '<dd>' + $rootScope.jsonPrint(obj[key]) + '</dd>';
            }
            printed += '</dl>';
        }
        else {
            printed = obj;
        }
        return printed;
    };


    $rootScope.empty = function(value) {
        return $.isEmptyObject(value);
    };

});


app.config(function($provide) {
    if (DEBUG) {
        $provide.decorator("$exceptionHandler", function($delegate) {
            return function(exception, cause) {
                $delegate(exception, cause);
                alert(exception.message+'\n'+exception.stack);
            };
        });
    }
});

// From https://github.com/gkappel/demo-d201305/
app.factory('ModelUtils', function($http, $log, $filter) {
    var handleErrors = function(serverResponse, status, errorDestination) {
        if (angular.isDefined(errorDestination)) {
            if (status >= 500) {
                errorDestination.form = 'Server Error: ' + status;
            } else if (status >= 401) {
                errorDestination.form = 'Unauthorized Error: ' + status;
            } else {
                angular.forEach(serverResponse, function(value, key) {
                    if (key != '__all__') {
                        errorDestination[key] = angular.isArray(value)
                            ? value.join("<br/>") : value;
                    } else {
                        errorDestination.form = errorDestination.form || ''
                            + key + ':' + angular.isArray(value) ?
                            value.join("<br/>") : value;
                    }
                });
            }
        }
    };



    var ModelUtils = {

        preSerialize: function(obj) {
            obj = typeof obj !== 'undefined' ? obj : {};
            var objs = angular.copy(obj);
            if (!(objs instanceof Array)) { // C'est un objet
                angular.forEach(objs, function(value, key) {
                    if ((value instanceof Date) && key != 'debut' && key != 'fin') {
                        objs[key] = $filter("date")(value, "dd/MM/yyyy");//"yyyy-MM-dd");
                    }
                });
            }
            else {
                for (var value, i=0; i<objs.length; i++) {
                    value = objs[i];
                    if ((value instanceof Date)) {
                        objs[i] = $filter("date")(value, "dd/MM/yyyy");//"yyyy-MM-dd");
                    }
                }
            }
            return objs;
        },

        load: function(name, params) {
            return $http.get('/api/'+name+'/', {params:this.preSerialize(params)})
                .then(function(response) {
                return response.data;
            });
        },
        get: function(name, uid) {
            //$log.log("ModelUtils.get('/api/"+name+"/"+uid+"/')");
            return $http.get('/api/'+name+'/'+uid+'/').
                then(function(response){
                    return response.data;});
        },
        create: function(name, obj, errors) {
            //errors.form = null;
            if (errors.hasOwnProperty('form')) {
                delete errors.form;
            }
            return $http.post('/api/'+name+'/', obj).
                success(function(response, status, headers, config) {
                    angular.extend(obj, response);
                }).
                error(function(response, status, headers, config) {
                    handleErrors(response, status, errors);
                });
        },
        save: function(name, action, obj, errors) {
            if (errors.hasOwnProperty('form')) {
                delete errors.form;
            }
            var pk = (angular.isDefined(obj.uid) && obj.uid)
                    || (angular.isDefined(obj.id) && obj.id);
            if (!pk) {
                return this.create(name, obj, errors);
            }
            var url = '/api/' + name + '/' + pk + '/';
            if (action) {
                url += action + '/';
            }
            return $http.put(url, obj).
                success(function(response, status, headers, config) {
                    angular.extend(obj, response);
                }).
                error(function(response, status, headers, config) {
                    handleErrors(response, status, errors);
                });
        },
        del: function(name, obj, params) {
            params = typeof params !== 'undefined' ? params : {};
            return $http.delete('/api/'+name+'/' + obj.uid + '/', {params:params});
        }
    };
    return ModelUtils;
});


app.factory('top', function($rootScope, $http, $cookies) {
    // attention, ce n'est pas le TopCtrl
    var top =  {
    };
    var build_entity = function (data) {
        var ret = {};
        ret.values = [];
        ret.by_uid = {};
        ret.by_cle = {};
        //data.unshift({uid:0,nom:'Indéfini',cle:''});
        for (var i=0,entity;i<data.length;i++) {
            entity = data[i];
            ret.by_uid[entity.uid] = {
                nom : entity.nom,
                cle : entity.cle
            };
            ret.values.push(entity);
        };
        return ret;
    };


    angular.forEach(ENTITIES, function(e) {
        $http.get('/api/entity/'+e+'/').then(function(response) {
            top.entities[e] = build_entity(response.data);
        });
    });

    top.entities['statut'] = build_entity([
        {uid:-1,nom:'Supprimé',cle:'supprime'},
        {uid:0,nom:'Valide',cle:'valide'},
        {uid:1,nom:'Validation V1',cle:'validation_v1'},
        {uid:2,nom:'À traiter',cle:'a_traiter'}
    ]);

    return top;
});



app.filter('entity', function(){
    // ((bon.demande.type_demande|entity:entities.type_demande:"uid":"nom" ))
    return function(value, name, from, to) {
        from = typeof from !== 'undefined' ? from : "uid";
        to = typeof to !== 'undefined' ? to : "nom";
        if (value != null) {
            if (this.top.entities[name]['by_'+from].hasOwnProperty(value))
                value = this.top.entities[name]['by_'+from][value][to];
        }
        if (value) {
            return value;
        }
        return "";
    };
});

app.filter('getNom', function(){
    return function(obj, key) {
        if (typeof obj !== 'undefined' && angular.isObject(obj)
            && obj.hasOwnProperty(key) && obj[key]) {
            return this.top.entities[key].by_uid[obj[key]].nom;
        }
        return '';
    };
});

app.filter('getCle', function(){
    return function(obj, key) {
        if (typeof obj !== 'undefined' && angular.isObject(obj)
            && obj.hasOwnProperty(key) && obj[key]) {
            return this.top.entities[key].by_uid[obj[key]].cle;
        }
        return '';
    };
});

app.directive('inverted', function() {
    // Voir user_form.html
    return {
        require: 'ngModel',
        link: function(scope, element, attrs, ngModel) {
            ngModel.$parsers.push(function(val) { return !val; });
            ngModel.$formatters.push(function(val) { return !val; });
        }
    };
});

