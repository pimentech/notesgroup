import socket
import os
import globals

DEVELOPMENT_ENVIRON = os.environ.get('DJDEV', None)
VIRTUAL_HOST = os.environ.get('VIRTUAL_HOST')
HOSTNAME = socket.gethostname()


if socket.gethostbyname("safran.pimentech.net") == '192.168.1.2':
    DBHOST = "chili"
else:
    DBHOST = "localhost"


DATABASES = {
    'default': {
        'ENGINE' : 'django.db.backends.postgresql_psycopg2',
        'NAME' : globals.DBNAME,
        'HOST' : DBHOST,
        'PASSWORD' : globals.DBPWD,
        'PORT' : globals.DBPORT,
        'USER' : globals.DBUSER
    }
}

FS_STORAGE_PATH = '/var/notesgroup'

HTTP_STATIC = '/static'
HTTP_ROOT = 'http://notesgroup.pimentech.net'
HOME = '/home/notesgroup'
DEBUG = False
STATIC_DIR = 'globals.STATICDIR'
TEMPLATE_DIRS = (HOME + '/django_templates', )

if DEVELOPMENT_ENVIRON:
    HOME = os.environ.get('HOME')
    INTERNAL_IPS = (
        '127.0.0.1',
        '192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4', '192.168.1.5',
        '192.168.1.6', '192.168.1.7', '192.168.1.8', '192.168.1.9', '192.168.1.10',
        '192.168.1.11', '192.168.1.12', '192.168.1.13', '192.168.1.14', '192.168.1.15',
        '192.168.1.16', '192.168.1.17', '192.168.1.18', '192.168.1.19', '192.168.1.20',
        '192.168.1.21', '192.168.1.22')

    FS_STORAGE_PATH = '/tmp'

    TEMPLATE_DIRS = ('templates', )

    HTTP_ROOT = 'http://origan:8010'
    STATIC_DIR = os.getcwd() + '/static/'
DEBUG = True

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = 'http://pimente.ch/admin_media/'



STATIC_URL = HTTP_STATIC + '/'
STATICFILES_DIRS = (STATIC_DIR,)
