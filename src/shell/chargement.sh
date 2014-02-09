#! /bin/bash

if [ -f <CONFIGDIR>/globals?*.sh ]
then
	. <CONFIGDIR>/globals?*.sh
else
	. <CONFIGDIR>/globals.sh
fi

case $DEBUG in
  1) set -x
     ;;
  *)
     ;;
esac

date=`date '+%Y-%m-%d'`
export LOGFILE=${LOGDIR}/notesgroup.log

error() {
		echo "ERROR:chargement.sh:$date: $1" 1>&2
		echo "ERROR:chargement.sh:$date: $1" >> $LOGFILE
}

test=0

TMPDIR=/tmp/`whoami`
mkdir -p ${TMPDIR}
if [ $? -ne 0 ]
then
	error "cannot mkdir -p ${TMPDIR}"
	exit 1
fi

if [ -f ${TMPDIR}/chargement_notes.lock ]
then
	error "chargement.sh already running ..."
	exit 1
fi

touch ${TMPDIR}/chargement_notes.lock

while true
do
  case $1 in
    -t)	test=1
		shift 1
		;;
     *)
		break
		;;
  esac
done

srcdb=${DBNAME}@${DBHOST}
DUMPDIR=/home/${CRONUSER}/dump/
mkdir -p $DUMPDIR
err=0


exec-sql.sh -H ${DBHOST} -d ${DBNAME} -u "${DBUSER}" -p "${DBPWD}" -c "vacuum full analyze;" -l $LOGFILE -o /dev/null
if [ $? -ne 0 ]
then
	error "cannot vacuum in $srcdb"
fi

find ${DUMPDIR} -name 'dump_${srcdb}_*.sql.gz' -mtime +15 -exec rm -f {} \; -print >> $LOGFILE;

echo "`date` : dump $srcdb"
dump=${DUMPDIR}/dump_${srcdb}_${date}.sql.gz
dump-db.sh -H ${DBHOST} -d ${DBNAME} -u "${DBUSER}" -p "${DBPWD}" -l $LOGFILE | gzip > $dump
if [ $? -ne 0 ]
then
	error "cannot dump $srcdb"
	err=1
fi

savelog -c 7 ${LOGFILE}

rm -f ${TMPDIR}/chargement_notes.lock

exit $err
