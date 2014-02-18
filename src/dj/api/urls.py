from django.conf.urls.defaults import patterns, url
import views

urlpatterns = patterns(
    '',
    url(r'^note/$', views.NoteList.as_view()),
    url(r'^note/(?P<pk>\d+)/$', views.NoteElement.as_view()),
    url(r'^sub_tree/(?P<pk>\d+)/$', views.SubTree.as_view()),
)
