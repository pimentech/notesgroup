# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


commonpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    (r'', include('dj.notesgroup.urls')),
)

if settings.DEVELOPMENT_ENVIRON:
    urlpatterns = patterns(
        '',
        (r'^static/pimentech/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.HOME + '/src/scripts/src/'}),
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.STATIC_DIR}),
        (r'^pimentech/img/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.HOME + '/src/scripts/src/images/'}),
        (r'^pimentech/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.HOME + '/src/scripts/src/'}),
    ) + commonpatterns
else:
    urlpatterns = commonpatterns
