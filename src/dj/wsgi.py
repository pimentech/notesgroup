import os, sys
import traceback

sys.stdout = sys.stderr

sys.path = ['/home/samusocial/config','/home/samusocial/lib/python/'] + sys.path

os.environ['DJANGO_SETTINGS_MODULE'] = 'dj.settings'
import django.core.handlers.wsgi

try:
    application = django.core.handlers.wsgi.WSGIHandler()
except:
	traceback.print_exc(sys.stderr)

