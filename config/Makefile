include ../rules/make.rules
include globals.mak

SRCS = globals.mak ${wildcard globals?*.mak}
GLOBALFILES = ${SRCS:.mak=.py} ${SRCS:.mak=.pyo} ${SRCS:.mak=.pyc} ${SRCS:.mak=.sh} apache.conf
SPECFILES = ${wildcard *.ncftp} ${wildcard *.pem} 

DIRS = ${LOGDIR} ${CONFIGDIR} ${DUMPDIR} ${DESTIMAGEDIR}
all: ${GLOBALFILES}

clean:
	@echo "cleaning"
	@rm -rf ${GLOBALFILES} *~ *.ok replace_bak *.lst apache.conf

install: all install.ok

install.ok: ${SRCS} ${GLOBALFILES}  ${SPECFILES} ${DIRS}
	@echo "installing global files"
	@cp ${SRCS} ${GLOBALFILES} ${SPECFILES} ${CONFIGDIR}
	@echo "** don't forget to reload crontab of ${CRONUSER} **"
	@touch $@

${CONFIGDIR}:
	@echo "creating $@"
	@mkdir -p $@
	@chmod o-rwx $@
	@if [ "$$(whoami)" = "root" ] ; \
	then \
		chown ${CRONUSER}.www-data $@ ; \
	else \
		echo "ask your administrator to make $@ belongs to group www-data" ; \
	fi

${LOGDIR}:
	@echo "creating $@"
	@mkdir -p $@
	@chmod o-rwx $@

${DUMPDIR}:
	@echo "creating $@"
	@mkdir -p $@
	@chown ${CRONUSER}. $@
	@chmod o-rwx $@

${DESTIMAGEDIR}:
	@echo "doing $@"
	@mkdir -p $@
	@if [ "$$(whoami)" = "root" ] ; \
	then \
		chown ${CRONUSER}.www-data $@ ; \
	else \
		echo "ask your administrator to make $@ belongs to group www-data" ; \
	fi
	@chmod -R g+w $@

apache.conf: globals.mak
	@echo "PythonPath \"['${CONFIGDIR}','${PYTHONDIR}','${PYTHONDIR}/dj/apache'] + sys.path\"" > $@  

