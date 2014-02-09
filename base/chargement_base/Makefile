include ../../rules/make.rules

GLOBALSFILE=globals.mak
include ../../config/${GLOBALSFILE}

LSTFILES = ${wildcard ${SRCLSTDIR}/type_*.lst} ${SRCLSTDIR}/etat_note.lst
TYPESUFFIX=.lst

SQLFILES = tables.sql ${LSTFILES:${SRCLSTDIR}/%.lst=%.sql}
LOADFILES = ${SQLFILES:.sql=.ok}
VPATH=.:${SRCLSTDIR}

all: ${SQLFILES}
	@echo "doing $@"

install: all ${LOADFILES} vital.ok
	@echo "done"

.sql.ok:
	@echo "loading $@"
	@exec-sql.sh -u ${DBUSER} -p ${DBPWD} -d ${DBNAME} -H ${DBHOST} -l ${SRCLOG} -f $< -o $@.tmp
	@mv $@.tmp $@

.lst.sql:
	@echo "doing `basename $@`"
	@echo "delete from `basename $< ${TYPESUFFIX}` where uid <> 0;" > $@.tmp
	@export table=`basename $< ${TYPESUFFIX}`; sed '/^$$/d' $< | \
	awk -F'|' "BEGIN { OFS=\"','\" } { print \"insert into $${table} (uid, nom, codecrea) values ('\"\$$1,\$$2,\"Makefile');\" }" >> $@.tmp
	@mv $@.tmp `basename $@`

remplissage.ok: ${SRCSQLDIR}/debug_remplissage.sql
	@echo "doing $@"
	@exec-sql.sh -u ${DBUSER} -p ${DBPWD} -f $< -d ${DBNAME} -H ${DBHOST} -l ${SRCLOG} -o $@.tmp
	@mv $@.tmp $@

vital.ok: ${SRCSQLDIR}/vital_chargement.sql
	@echo "doing $@"
	@exec-sql.sh -u ${DBUSER} -p ${DBPWD} -f $< -d ${DBNAME} -H ${DBHOST} -l ${SRCLOG} -o $@.tmp
	@mv $@.tmp $@

clean:
	rm -f *.ok *~ *.lst *.sql *.log *.tmp*

tables_type_user.lst:
	@echo "doing $@"
	@exec-sql.sh -u ${DBUSER} -p ${DBPWD} -c "\d" -d ${DBNAME} -H ${DBHOST} -l ${SRCLOG} -o $@

alltables.lst: tables_type_user.lst
	@echo "doing $@"
	@awk -F'|' '{ print $$1 }' $< > $@

tables.lst: alltables.lst
	@echo "doing $@"
	grep -v droits $< | grep -v '_seq$$' > $@

tables.sql: tables.lst
	@echo "doing $@"
	@echo "BEGIN;" > $@
	@for table in `awk -F'|' '{ print $$1 }' $<` ; \
	do \
		echo "delete from $${table} where uid=0;" >> $@ ; \
		echo "insert into $${table} (uid,nom,codecrea) values (0,'indefini','Makefile');" >> $@ ; \
	done
	@echo "COMMIT;" >> $@