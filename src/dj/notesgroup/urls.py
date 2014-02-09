# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url, include
from django_pimentech.viewsobjects import ObjectCaller

from dj.notesgroup import views

urlpatterns = patterns(
    '',
    url(r'^$', ObjectCaller(views.IndexView)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
    url(r'^workgroup/$', ObjectCaller(views.WorkGroupView)),
    url(r'^group/(?P<societe>\d+)/(?P<action>edit)/$',
        ObjectCaller(views.SocieteEditView)),
    url(r'^group/(?P<action>new)/$', ObjectCaller(views.SocieteEditView)),
    url(r'^user/(?P<_user_edit>\d+)/(?P<action>edit)/$',
        ObjectCaller(views.UserEditView)),
    url(r'^user/(?P<action>edit)/$', ObjectCaller(views.UserEditView)),
    url(r'^user/(?P<societe>\d+)/(?P<action>new)/$',
        ObjectCaller(views.UserEditView)),
    url(r'^tree/$', ObjectCaller(views.SubTreeView)),
    url(r'^treej/$', ObjectCaller(views.SubTreeJSON)),
    url(r'^tree/(?P<note>\d+)/$', ObjectCaller(views.SubTreeView)),
    url(r'^treej/(?P<note>\d+)/$', ObjectCaller(views.SubTreeJSON)),
    url(r'^jframe_list$', ObjectCaller(views.NoteListView)),
    url(r'^(?P<note>\d+)/detail_list/$', ObjectCaller(views.DetailListView)),
    url(r'^(?P<note>\d+)/(?P<action>edit|new)/$',
        ObjectCaller(views.NoteEditView)),
    url(r'^(?P<note>\d+)/add_comment/$',
        ObjectCaller(views.NoteAddCommentView)),
    url(r'^(?P<note>\d+)/detail/$', ObjectCaller(views.NoteDetailView)),
    url(r'^(?P<note>\d+)/detail_new_window/$',
        ObjectCaller(views.NoteDetailNewWindowView)),
    url(r'^(?P<note>\d+)/diff/', ObjectCaller(views.NoteDiffView)),
    url(r'^(?P<note>\d+)/users/$', ObjectCaller(views.NoteUsersView)),
    url(r'^(?P<note>\d+)/move_to/(?P<new_parent>\d+)/$',
        ObjectCaller(views.NoteMoveView)),

    url(r'^(?P<note>\d+)/timer/(?P<timer>\d+)/',
        ObjectCaller(views.TimerEditView)),
    url(r'^(?P<note>\d+)/timer/',
        ObjectCaller(views.TimerEditView)),
    url(r'^(?P<note>\d+)/set_timer/',
        ObjectCaller(views.SetTimerView)),
    url(r'^get_timer_day/',
        ObjectCaller(views.GetTimerDayView)),



    (r'^i18n/', include('django.conf.urls.i18n')),
    # changement de password par l'utilisateur loggue
    url(r'^password_change/$', 'django.contrib.auth.views.password_change'),
    url(r'^password_change/done/$',
        'django.contrib.auth.views.password_change_done'),
    # reset du password ( si perte par ex)
    url(r'^password_reset_request/$',
        'django.contrib.auth.views.password_reset'),
    url(r'^password_reset_done/$',
        'django.contrib.auth.views.password_reset_done'),
    url(r'^password_reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm'),
    url(r'^password_reset_complete/$',
        'django.contrib.auth.views.password_reset_complete'),

    url(r'^notes$', ObjectCaller(views.NoteListJsonView)),
)
