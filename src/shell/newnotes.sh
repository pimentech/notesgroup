#!/bin/bash

usage() {
	echo 'newnotes.sh -l login [ -n "real name" ]'
}

LOGIN=""
NAME=""

while true
  do
  case $1 in
	  -l)
		  LOGIN=$2
		  shift 2
		  ;;
	  -n) 
		  NAME=$2
		  shift 2
		  ;;
	  -h)  
		  usage
		  exit 1
		  ;;
	  *)
		  break
		  ;;
  esac
done

# Login obligatoire
if [ -z "$LOGIN" ]
	then
	usage
	echo "  Login absent"
	exit 1
elif test `echo $LOGIN | wc -w` -ne 1
	then
	usage
	echo "  Le login doit etre constitué d'un mot unique."
	exit 1
fi

echo "* checking for files..."
if [ ! -d /root/src/notesgroup/ ]
	then
	echo "Répertoire /root/src/notesgroup/ introuvable"
	exit 1
fi


GLOBALS=globals_notesgroup_$LOGIN
DESTHOME=/home/$LOGIN

# Creation des mots de passes (cryptes et non cryptes)
passwds=`makepasswd --chars=6 --crypt`
passwd=`echo $passwds | awk '{print($1)}'`
cryptedpasswd=`echo $passwds | awk '{print($2)}'`

useradd -m -p "$cryptedpasswd" -c "$NAME" $LOGIN
		
cd /root/src/notesgroup/config/

make

sed -e "s/^DBUSER;.*/DBUSER;ng_$LOGIN;/" -e "s/^DBNAME;.*/DBNAME;ng_$LOGIN;/" -e "s/^DBPWD;.*/DBPWD;$passwd;/" globals.lst > $GLOBALS.lst

make install

mkdir -p $DESTHOME/config/notesgroup/ $DESTHOME/log_apache/
ln -s /usr/local/notesgroup/config/$GLOBALS.sh $DESTHOME/config/notesgroup/$GLOBALS.sh

chown -R $LOGIN $DESTHOME

cd /root/src/notesgroup/base/generation_base
make clean
make GLOBALSFILE=$GLOBALS.mak install
cd /root/src/notesgroup/base/chargement_base
make clean;cvs up
make GLOBALSFILE=$GLOBALS.mak install

. $DESTHOME/config/notesgroup/$GLOBALS.sh

exec_sql() {
	exec-sql.sh -t 30 -H ${DBHOST} -d ${DBNAME} -u "${DBUSER}" -p "${DBPWD}" -l exec.log -c "$1" | dos2unix -f -- 
}

exec_sql "update userid set login = '"$LOGIN"' where login='admin'";

echo "Il ne reste plus qu'a creer une instance de NotesGroup dans Zope dans un repertoire $LOGIN avec l'ID notesgroup."



