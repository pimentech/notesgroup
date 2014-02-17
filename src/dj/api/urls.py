from django.conf.urls.defaults import patterns, url
from rest_framework.routers import DefaultRouter
import views
from django.views.decorators.cache import cache_page


urlpatterns = patterns(
    '',

    url(r'^note/$', views.NoteList.as_view()),
    url(r'^note/(?P<pk>\d+)/$', views.NoteElement.as_view()),

)
