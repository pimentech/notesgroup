include ../../rules/make.rules

GLOBALSFILE=globals.mak
include ../../config/${GLOBALSFILE}

all :  ${APPLICATION}.sql vital.sql
	@echo "doing $@"

clean :
	@echo "doing $@"
	@rm -f *~ *.tmp *.sql *.ok *.pgml *.sdot *.dot *.pdf *.eps *.ssql *.spgml *.rdot

install : all vital.ok
	@echo "doing $@"

${APPLICATION}.pgml: ${SRCXMLDIR}/${APPLICATION}.pgml
	@echo "doing $@"
	@cp -f $< $@

destroy.ok:
	@if [ -f create.ok ] ;\
	then \
		echo "doing $@" ;\
		destroy-db.sh -u ${DBUSER} -p ${DBPWD} -d ${DBNAME} -H ${DBHOST} -l ${SRCLOG} ;\
		date > $@ ;\
	fi

create.ok: destroy.ok createuser.ok
	@echo "doing $@"
	@create-db.sh -u ${DBUSER} -p ${DBPWD} -d ${DBNAME} -H ${DBHOST} -l ${SRCLOG} -E UTF8
	@date > $@

schema.ok: ${APPLICATION}.sql create.ok ${APPLICATION}.sql
	@echo "doing $@"
	@exec-sql.sh -u ${DBUSER} -p ${DBPWD} -f ${APPLICATION}.sql -d ${DBNAME} -H ${DBHOST} -l ${SRCLOG} -o $@.tmp
	@mv $@.tmp $@

vital.ok: schema.ok vital.sql
	@echo "doing $@"
	@exec-sql.sh -u ${DBUSER} -p ${DBPWD} -f vital.sql -d ${DBNAME} -H ${DBHOST} -l ${SRCLOG} -o $@.tmp
	@mv $@.tmp $@

vital.sql: ${SRCSQLDIR}/vital_generation.sql
	@echo "doing $@"
	@cp -f $< $@

plpgsql.sql: ${SRCSQLDIR}/plpgsql.sql
	@echo "doing $@"
	@cp -f $< $@

createuser.ok:
	@echo "doing $@"
	@read -p 'entrez le password postgres : ';create-user.sh -H ${DBHOST} -u ${DBUSER} -p ${DBPWD} -U postgres -P $${REPLY} -l ${SRCLOG} -d
	@date > $@

dropuser.ok:
	@echo "doing $@"
	@read -p 'entrez le password postgres : ';drop-user.sh -H ${DBHOST} -u ${DBUSER} -U postgres -P $${REPLY} -l ${SRCLOG}
	@date > $@

plpgsql.ok: plpgsql.sql vital.ok
	@echo "doing $@"
	@read -p 'entrez le password postgres : ';exec-sql.sh -u postgres -p "$${REPLY}" -f plpgsql.sql -d ${DBNAME} -H ${DBHOST} -l ${SRCLOG} -o $@.tmp
	@mv $@.tmp $@
