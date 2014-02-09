include ../../rules/make.rules

SHELLFILES = ${wildcard *.sh}

all:

clean:
	@rm *~ *.ok

install: all install.ok

install.ok: ${SHELLDIR} ${SHELLFILES}
	@echo "installing ${SHELLFILES}"
	@cp -u ${SHELLFILES} ${SHELLDIR}
	@${REPLACE} -r '<CONFIGDIR>' -s '${CONFIGDIR}' -f '${SHELLDIR}/*.sh'
	@chmod a+x ${SHELLDIR}/*.sh
	@date > $@
	@echo "You should add '*/5 * * * * nice -10 ${SHELLDIR}/send_alarm.sh' in a crontab."

${SHELLDIR}:
	@echo "creating $@"
	@mkdir -p $@
