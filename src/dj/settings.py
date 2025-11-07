# -*- coding: utf-8 -*-
# Django settings for samusocial project.

from local_settings import *
#CSRF_COOKIE_NAME = "XSRF-TOKEN"

TEMPLATE_DEBUG = DEBUG

ADMINS = (
     ('PimenTech', 'root@pimentech.net'),
)


MANAGERS = ADMINS

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'Europe/Paris'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15

LANGUAGES = (
    ('fr', ('French')),
)


PASSWORD_HASHERS = (
    # 'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    # 'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    # 'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)


LANGUAGE_CODE = 'fr-fr'
USE_I18N = True
USE_L10N = True

DATE_FORMAT = 'j N  Y'
DATETIME_FORMAT = 'j N  Y à H:i'
TIME_FORMAT = 'H:i'
SITE_ID = 1


#DATE_INPUT_FORMATS = ('%Y-%m-%d','%d/%m/%y')



# Make this unique, and don't share it with anybody.
SECRET_KEY = '+))r(&%-_ro926k&k=fu6gx38+j@cgwopkr=dhk^w2)#pq%61k'

AUTH_PROFILE_MODULE = 'notesgroup.Employe'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    )

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.request',
	)

MIDDLEWARE_CLASSES = (
	'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django_pimentech.middleware.ext.SQLLogToConsoleMiddleware',
)

ROOT_URLCONF = 'dj.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
	'dj.notesgroup',
    'django.contrib.admin',
)


SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#DEFAULT_FILE_STORAGE = 'django_pimentech.filesystemstorage.OverwriteStorage'

LOGIN_REDIRECT_URL = '/'


if DEVELOPMENT_ENVIRON and False:
    # https://github.com/dcramer/django-devserver
    # pip install git+git://github.com/dcramer/django-devserver#egg=django-devserver
    INSTALLED_APPS += 'devserver',
    DEVSERVER_IGNORED_PREFIXES = ['/static', '/css', '/js' ]
    DEVSERVER_TRUNCATE_SQL = True

    DEVSERVER_MODULES = (
        'devserver.modules.sql.SQLRealTimeModule',
        # 'devserver.modules.sql.SQLSummaryModule',
        # 'devserver.modules.profile.ProfileSummaryModule',

        # Modules not enabled by default
        #'devserver.modules.ajax.AjaxDumpModule',
        #'devserver.modules.profile.MemoryUseModule',
        #'devserver.modules.cache.CacheSummaryModule',
        #'devserver.modules.profile.LineProfilerModule',
        )

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
#SERVER_EMAIL = 'www-data@' + INTERNET_HOST
EMAIL_SUBJECT_PREFIX = '[NotesGroup] '

REST_FRAMEWORK = {
    #'DATE_FORMAT' : "%d/%m/%Y",
    'DATE_INPUT_FORMATS' : ['iso-8601', "%Y-%m-%dT%H:%M:%S.%fZ", "%d/%m/%Y", "%Y-%m-%d"],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}


