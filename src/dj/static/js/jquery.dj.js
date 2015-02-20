// -*- coding: utf-8 -*-
var global_edit_note;
var selected_treecell;
var tree_closed_class = "fa-plus-square-o";
var tree_open_class = "fa-minus-square-o";

function switchFromTo(id) {
	var dem = $("#id_"+id+"-demandeur_employe").get(0);
	var resp = $("#id_"+id+"-responsable_employe").get(0);
	var i = dem.selectedIndex;
	dem.selectedIndex = resp.selectedIndex;
	resp.selectedIndex = i;
}


function usersStr() {
	$('user').each(function () {
                       var user, name, elem;
                       elem = $(this);
                       user = elem.html();
                       if (employe_dict.hasOwnProperty(user)) {
                           name = employe_dict[user].name;
                           if (name) {
                               elem.replaceWith('<span title="'
                                                + employe_dict[user].tel
                                                + '">' + name + "</span>");
                           }
                       }
                   });
}


function humanPathFromTree(id) {
	var human_path = '';
	$('#id_tree_' + id).
		parents('div[uid]').
		find('tr:first td.cell a:first').
		each(function(i,e) {
                 human_path = $(e).text() + '/' + human_path;
             });
	return '/' + human_path;
}


function showNotes() {
	$("#societes").hide();
	$("#utilisateurs").hide();
	$("#notes").show();
}


function showMessage(text) {
	$('#message').html(text);
	$('#message').fadeIn();
	$('#message').fadeOut(2000);
}

function doneMessage() {
    showMessage("Modifications effectuées");
}



function errorMessage() {
	$('#message').html("Erreur !");
	$('#message').fadeIn();
}


function processingMessage() {
	$('#message').html("Traitement en cours...");
	$('#message').fadeIn();
}


function openNodes(ids, callback) {
	var id = ids.shift();
	if (id || id === 0) {
		var tree = $("#tree_" + id);
		var img = $("#img_" + id);
		if (img && img.hasClass(tree_closed_class)) {
			tree.hide();
			tree.load("/tree/" + id + "/", function () {
                tree.slideDown();
                tree.activateJFrame();
                img.removeClass(tree_closed_class)
                    .addClass(tree_open_class);
                openNodes(ids, callback);
            } );
		}
		else {
			openNodes(ids, callback);
		}
	}
	else {
		if (callback) {
			callback();
		}
	}
}

function openNode(id) {
	openNodes([id]);
}


function loadHideSubTree(id) {
	var tree = $("#tree_" + id);
	var img = $("#img_" + id);
	if (img.length) {
		if (img.hasClass(tree_closed_class)) {
			openNode(id);
		}
		else {
			tree.slideUp();
			tree.empty();
            img.removeClass(tree_open_class)
                .addClass(tree_closed_class);
		}

	}
}

function loadSubTree(id) {
	var img = $("#img_" + id);
	if (img.length) {
		img = img[0];
		if (img.hasClass(tree_open_class)) {
			loadHideSubTree(id);
		}
		loadHideSubTree(id);
	}
}


function loadHideUsers(id, path) {
	var users = $("#note-users-list-" + id);
	if (users.css("display") == "none") {
		users.load(path + "/users_list");
	}
	users.toggle();
}



function openTree(path, callback) {
	var id;
	do {
		id = path.shift();
	} while (path.length && parseInt(id,10).toString() != id);
	if (id) {
		path.unshift(id);
		openNodes(path, callback);
	}
}


function selectTreeCellParent(path) {
	if ($("#img_0")) {
		path = '/0' + path;
	}
	if (selected_treecell) {
		$("#" + selected_treecell).removeClass('selected');
	}
	path = path.split('/');
	path.pop(); // we want the parent
	selected_treecell = "cell_" + path.pop();
	openTree(path, function() { $("#" + selected_treecell).toggleClass('selected'); });
}

function resetForm() {
	$('#id_etat_note').val(-1).change();
	$('#id_demandeur').val(0).change();
	$('#id_timer_actor').val(0).change();
	$('#id_responsable').val(0).change();
	$('#id_path').val(0).change();
	$('#id_date_start').val('').change();
	$('#id_date_end').val('').change();
}



function goSearch(uid) {
	resetForm();
	$('#id_page').val("1").change();
	$('#id_chemin').val(uid).change();
	$("#html_chemin_txt").html($("#id_tree_"+uid).html());
	$("#id_path_label").show();
	$('#id_path').val('ici').change();
	$('#search_button').click();
	var seltreecell = "cell_" + uid;
	if (seltreecell != selected_treecell) {
		$("#" + selected_treecell).removeClass('selected');
		selected_treecell = seltreecell;
		$("#" + selected_treecell).addClass('selected');
	}
}


function goPage(page) {
	$('#id_page').val(page);
	$('#search_button').click();
	$('#id_page').val("1");
}


function goPartout() {
	$('#id_chemin').val('').change();
	$('#id_date_start').val('').change();
	$('#id_date_end').val('').change();
	$("#label_path").hide();
	$('#id_path').val('partout');
	$('#id_etat_note').val(1).change();
	if (selected_treecell) {
		$("#" + selected_treecell).removeClass('selected');
		selected_treecell = null;
	}

	$('#search_button').click();
}



function goTodo(uid) {
	$('#id_demandeur').val(0).change();
	$('#id_responsable').val(uid).change();
	$('#id_timer_actor').val(0).change();
	goPartout();
}

function goTouched(uid) {
	$('#id_chemin').val('').change();
	$('#id_date_start').val('').change();
	$('#id_date_end').val('').change();
	$("#label_path").hide();
	$('#id_path').val('partout');
	$('#id_etat_note').val("0").change();
	$('#id_demandeur').val(0).change();
	$('#id_responsable').val(0).change();
	$('#id_timer_actor').val(uid).change();
	if (selected_treecell) {
		$("#" + selected_treecell).removeClass('selected');
		selected_treecell = null;
	}

	$('#search_button').click();
}



function goAsked(uid) {
	$('#id_demandeur').val(uid).change();
	$('#id_responsable').val(0).change();
	$('#id_timer_actor').val(0).change();
	goPartout();
}

function highlightInput() {
	var highlight = false;
	if (this.tagName == 'INPUT') {
		if (this.value) {
			highlight = true;
		}
	}
	else {
		// select
		if (this.value && this.value != '0') {
			highlight = true;
		}
	}
	if (highlight) {
		$(this).animate({ backgroundColor: "#68BFEF" }, 1000);
	}
	else {
		$(this).css("backgroundColor", "#DDDDDD");
	}
}


function launchWysiwyg(target) {
	target.tinymce(
		{
			script_url : http_static+'/pimentech/lib/tiny_mce/tiny_mce.js',
            language : 'fr', theme : "advanced",
            content_css : http_static+'/css/tinymce.css',
			theme_advanced_toolbar_location : "top", theme_advanced_toolbar_align : "left",
            theme_advanced_buttons1 : "mybutton,fontsizeselect,bold,italic,underline,separator,strikethrough,justifyleft,justifycenter,justifyright, justifyfull,bullist,numlist,undo,redo,link,unlink",
            theme_advanced_buttons2 : "", theme_advanced_buttons3 : "",
            paste_auto_cleanup_on_paste : true, paste_remove_styles: true, paste_remove_styles_if_webkit: true, paste_strip_class_attributes: true,
            plugins : "paste",
			setup : function(ed) {
				ed.addButton('mybutton', {
                                 title : 'My button',
                                 image : http_static+'/img/commentaire.gif',
                                 onclick : function() {
                                     var now = new Date();
                                     ed.focus();
                                     var str = "";
                                     str += '<div style="border:1px solid #CCCCCC;margin:1em 0 0;padding:0 1em" id="';
                                     str += now.getTime();
                                     str += '"><h6 style="background:none repeat scroll 0 0 White;display:inline;left:0;padding:0.5em;position:relative;top:-0.8em">';
                                     str += utilisateur_authentifie + ' ' + NOW;
                                     str += '</h6><p>&gt;&nbsp;</p></div>';
                                     ed.selection.setContent(str);
                                 }
                             });
			}


		});
}


function launchWysiwygNoQuote(target) {
	target.tinymce(
		{
			script_url : http_static+'/pimentech/lib/tiny_mce/tiny_mce.js',
            language : 'fr', theme : "advanced",
			theme_advanced_toolbar_location : "top", theme_advanced_toolbar_align : "left",
            theme_advanced_buttons1 : "mybutton,bold,italic,underline,separator,strikethrough,justifyleft,justifycenter,justifyright, justifyfull,bullist,numlist,undo,redo,link,unlink",
            theme_advanced_buttons2 : "", theme_advanced_buttons3 : "",
            paste_auto_cleanup_on_paste : true, paste_remove_styles: true, paste_remove_styles_if_webkit: true, paste_strip_class_attributes: true,
			plugins : "paste"
		});
}



function showHideDetail(span, path) {
	var target = $($(span).getJFrameTarget());
	var url;
	if (target.find("div.box").length) {
		target.loadJFrame(path + "/detail_list/");
	}
	else {
		target.loadJFrame(path + "/detail/");
	}
}


function newNote(parent_uid) {
    if ($('#new_note').length){
        return false;
    }
	$("#top-list-id").after('<div id="new_note" class="note-list"></div>');
	var target = $("#new_note");
	target.loadJFrame('/' + parent_uid + '/new/');
    return true;
}


function updateTimerDay() {
    $.get('/get_timer_day/', function(response) {
        var completed = 100/7.0*parseFloat(response) || 0;
        $("#progress_bar")
            .progressbar({ value: completed })
            .title(response + " h");
    });
}

function updateTimer(select, note_id) {
    var value = $(select).val();
    $.post('/'+note_id+'/set_timer/', 'duration='+value, function(response) {
        updateTimerDay();
    });
}


function resizeNotesGroup() {
	var h = $("#page").height() - 19;
	$(".content").height(h);
	$("#ngcontent").height(h-$("#search").height());
	$("#ngtree").height(h-$("#menu").height());
	$("#pub").css("top",h-5);
	$("#pub").css("left",$("#page").width()-95);
	$("#user_info").css("top",5);
	$("#user_info").css("left",$("#page").width()-95);
}

window.onresize = resizeNotesGroup;


function noteAddUser(note_id, id) {
	processingMessage();
	$("#note-users-list-"+ note_id)
        .loadJFrame('/' + note_id + '/users/?action=add&user=' + id,
                    function () {
                        $("#cell_" + note_id + " a").show();
                        doneMessage();
                    });
}

function setDroppableNotes(parent_id) {
	$('#' + parent_id).find(".img-note").droppable(
		{
            accept : '.dropaccept',
			activeClass: 'ui-state-active',
			hoverClass: 'ui-state-hover',
			tolerance: 'intersect',
			drop: function (event,ui) {
				processingMessage();
				var note = ui.draggable.attr('uid');
				var new_parent = $(this).parents("td.cell").attr("uid");
				$.get('/' + note + '/move_to/' + new_parent + '/', { },
                       function() {
                           $('#search_button').click();
                           $('#tree_parent_' + note).empty();
                           loadSubTree(new_parent);
                           doneMessage();
                       }
                     );
			}
		});

	$('#' + parent_id).find('.users-droppable').droppable(
		{
			accept : '.group-user',
			activeClass: 'dropactive',
			hoverClass: 'drophover',
			tolerance: 'intersect',
			drop: function (event,ui) {
				noteAddUser($(this).attr("uid"),
							ui.draggable.attr("uid"));
			}
		}
	);

}


function goAnchor(id) {
	var target_offset = $("#"+id).offset();
	var target_top = target_offset.top;
	$('#ngcontent').animate({scrollTop:target_top}, 500);
}

function copyToClipboard(text) {
   // Spawn an invisible text box (far outside the document),
   // put the text in and select it so that the user can copy
   // it with the platform specific key combination.

   text = text.replace('\s*:\s*', '-').replace(/\s*:\s*/g, '/').replace(/[ '"]/g, '_');
   $('<input type="text" class="hidden-copy-input">').appendTo('body')
     .css({ position: 'fixed', top: -1000000, left: -1000000 })
     .val(text)
     // Remove from DOM on unfocus
     .focusout(function() { $(this).remove(); })
     .select();
    showMessage('<i class="fa fa-copy"></i> Ctrl-C pour copier');
    return false;
}



jQuery(function($){
	$.datepicker.regional['fr'] = {
		closeText: 'Fermer',
		prevText: '&#x3c;Préc',
		nextText: 'Suiv&#x3e;',
		currentText: 'Courant',
		monthNames: ['Janvier','Février','Mars','Avril','Mai','Juin',
		'Juillet','Août','Septembre','Octobre','Novembre','Décembre'],
		monthNamesShort: ['Jan','Fév','Mar','Avr','Mai','Jun',
		'Jul','Aoû','Sep','Oct','Nov','Déc'],
		dayNames: ['Dimanche','Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi'],
		dayNamesShort: ['Dim','Lun','Mar','Mer','Jeu','Ven','Sam'],
		dayNamesMin: ['Di','Lu','Ma','Me','Je','Ve','Sa'],
		weekHeader: 'Sm',
		dateFormat: 'dd/mm/yy',
		firstDay: 1,
		isRTL: false,
		showMonthAfterYear: false,
		yearSuffix: ''};
	$.datepicker.setDefaults($.datepicker.regional['fr']);
});


