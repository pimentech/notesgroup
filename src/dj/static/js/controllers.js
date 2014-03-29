'use strict';
/* global angular, $, app, ENTITIES, USERNAME, USERID, EMP_L, build_entity */
function TopCtrl($scope, $cookies, $rootScope, $window, $location,
                 $log, top, $http, ModelUtils, $filter,
                 $anchorScroll) {
    $scope.top = top;

    $scope.node = null;
    $scope.tree = null;

    $scope.DEBUG = DEBUG;
    $scope.userid = USERID;
    $scope.emp_l = EMP_L;
    $scope.emp_d = {};

    var self = this;

    $scope.initialize = function(data) {
        angular.forEach(EMP_L, function(e) {
            $scope.emp_d[e.uid] = e;
        });
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



app.controller('NoteCtrl', function NoteCtrl(
    $scope, $filter, $rootScope, top, $log, ModelUtils, $injector, $sanitize) {
    $injector.invoke(TopCtrl,
                     this,
                     { $scope: $scope, top:top, $log:$log,
                       ModelUtils:ModelUtils }
                    );
    var self = this;
    $scope.name = 'note';

    $scope.limit = [ 0, 50, 100, 200 ];

    $scope.queryParams = {
        chemin : null, // Changer ce nom, c'est en fait l'id de recherche du noeud
        date_end: null,
        date_start: null,
        demandeur: 0,
        etat_note: 1,
        limit: 50,
        page: 1,
        path: 'partout',
        responsable: 2,
        sel_txt: 'resume',
        sort_on: 'datemodif',
        sort_order: '-',
        timer_actor: 0,
        timer_date:	null,
        txt: null
    };

    $scope.tree = null;
    $scope.treeOptions = {
        nodeChildren: "children",
        dirSelectable: true,
        injectClasses: {
            ul: "a1",
            li: "a2",
            liSelected: "a7",
            iExpanded:  "fa fa-minus-square-o",
            iCollapsed: "fa fa-plus-square-o",
            iLeaf: "a5",
            label: "a6",
            labelSelected: "a8"
        }
    };


    $scope.initialize = function() {
        angular.forEach(EMP_L, function(e) {
            $scope.emp_d[e.uid] = e;
        });
        ModelUtils.load("tree").then(function(res) {
            $scope.tree = top.tree = res;
        });
        $scope.load();
    };

    $scope.icon = {
        1:'home',
        2:'folder',
        3:'folder',
        4:'comment-o',
        5: 'phone',
        6: 'bug',
        7: 'question',
        0: 'comment',
        8: 'message'
    };

    $scope.load = function(event) {
        //$scope.query_params = $scope.serialize($scope.queryParams);
        ModelUtils.load("note", $scope.queryParams).then(function(res) {
            top.notes = res;
            angular.forEach(res, function(obj) {
                obj.showDetail = false;

            });
        });
    };


    $scope.save = function(note) {
        note.errors = {};
        ModelUtils.save($scope.name, '', note, note.errors);
    };



    $scope.goTodo = function() {
        $scope.queryParams.demandeur = 0;
        $scope.queryParams.responsable = $scope.userid;
        $scope.queryParams.timer_actor = 0;
        $scope.load();
    };

    $scope.goAsked = function() {
        $scope.queryParams.demandeur = $scope.userid;
        $scope.queryParams.responsable = 0;
        $scope.queryParams.timer_actor = 0;
        $scope.load();
    };

    $scope.goTouched = function() {
        $scope.queryParams.chemin = '';
        $scope.queryParams.date_start = '';
        $scope.queryParams.date_end = '';
        $("#label_path").hide();
        $scope.queryParams.path = 'partout';
        $scope.queryParams.etat_note = 0;
        $scope.queryParams.demandeur = 0;
        $scope.queryParams.responsable = 0;
        $scope.queryParams.timer_actor = $scope.userid;
        $scope.load();
    };


    $scope.showSelected = function(node_tree) {
        $scope.queryParams.chemin = node_tree.uid;
        $scope.queryParams.path = 'ici';
        $scope.queryParams.responsable = 0;
        $scope.queryParams.demandeur = 0;
        $scope.queryParams.etat_note = -1;
        $scope.load();
    };

    $scope.toggleDetail = function(note) {
        note.showDetail = !note.showDetail;
        if (note.showDetail) {
            ModelUtils.get("note", note.uid).then(function(res) {
                angular.extend(note, res);
            });
        }
    };

});
