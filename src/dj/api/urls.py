from django.conf.urls import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^tree/$', views.Tree.as_view()),
    url(r'^note/$', views.NoteList.as_view()),
    url(r'^note/(?P<pk>\d+)/$', views.NoteElement.as_view()),
    url(r'^note/(?P<pk>\d+)/timer/$', views.TimerCreate.as_view()),
    url(r'^timer/(?P<pk>\d+)/$', views.TimerElement.as_view()),
    url(r'^sub_tree/(?P<pk>\d+)/$', views.SubTree.as_view()),
)
