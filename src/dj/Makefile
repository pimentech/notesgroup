include ../../config/globals.mak
include ../../rules/make.rules

SRCXMLDIR = ../../src/xml
SRCCONFIGDIR = ../../config
LANGUAGES = en fr

VPATH=.:${SRCXMLDIR}:${SRCCONFIGDIR}
PYTHONPATH_DEV = ..:${HOME}/src/pimentech/libcommonDjango:${HOME}/src/libcommonDjango:${SRCCONFIGDIR}
PYTHONDIR = ${HOME}/lib/python
LOCALEDIR = ${PYTHONDIR}/dj/locale

all: # moel

clean:
	@find . -name "*~" -exec rm -f {} \;
	@rm karma.conf.*.js

install-python:
	@mkdir -p ${PYTHONDIR}
	@python setup.py install -O2 --home=${HOME}

install-static:
	@rsync -ar --cvs-exclude static/ ${STATICDIR}/

install-templates:
	@mkdir -p ${TEMPLATESDIR}
	@rsync -axr --delete --cvs-exclude templates/ ${TEMPLATESDIR}


install-apacheconf: ${APACHECONFDIR}
	@echo "installing apacheconf"
	@rsync -ar --delete --cvs-exclude apache/ ${APACHECONFDIR}/


${APACHECONFDIR}:
	@echo "creating $@"
	@mkdir -p $@


install: all install-python install-locale.ok install-templates install-static install-apacheconf
#	@cd ../shell && make install
	@echo "done"

syncdb:
	@python manage.py syncdb


locales:
	@export DJDEV=1 PYTHONPATH=${PYTHONPATH_DEV} && for lang in ${LANGUAGES}; do \
        python manage.py makemessages  -l $$lang; \
    done

compile-locale.ok:
	@echo "compiling locales"
	@for lang in ${LANGUAGES}; do \
		msgfmt -o locale/$$lang/LC_MESSAGES/django.mo locale/$$lang/LC_MESSAGES/django.po; \
	done
	@date > $@

install-locale.ok: compile-locale.ok
	@echo "installing django-all.po"
	@for lang in ${LANGUAGES}; do \
		mkdir -p ${LOCALEDIR}/$$lang/LC_MESSAGES; \
		cp locale/$$lang/LC_MESSAGES/django.mo ${LOCALEDIR}/$$lang/LC_MESSAGES/django.mo; \
	done
	@date > $@


shell:
	@python manage.py shell

syncdb-dev: globals.py
	@export DJDEV=1 PYTHONPATH=${PYTHONPATH_DEV} && python manage.py syncdb

ipython: globals.py
	@export DJDEV=1 PYTHONPATH=${PYTHONPATH_DEV} && ipython


ifndef PORT
	PORT=9001
endif
BROWSER="Chrome"

runserver-dev: globals.py
	@export DJDEV=1 PYTHONPATH=${PYTHONPATH_DEV} && python manage.py runserver 0:${PORT}

dbshell-dev: globals.py
	@export DJDEV=1 PYTHONPATH=${PYTHONPATH_DEV} && python manage.py dbshell

karma: test/e2e/vars.js
	@echo "starting karma with PORT=${PORT} and BROWSER=${BROWSER}"
	@BROWSER=${BROWSER} PORT=${PORT} karma start karma.conf.js


shell-dev: globals.py
	echo ${PYTHONPATH_DEV}
	@export DJDEV=1  PYTHONPATH=${PYTHONPATH_DEV} && python manage.py shell


