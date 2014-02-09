#!/bin/sh

# Lancé par cron pour provoquer l'envoie d'alarmes

LOCK=~/send_alarm.lock

case $DEBUG in
  1) set -x
     ;;
  *)
     ;;
esac

usage() {
	echo -e "usage : send_alarme -h host/URL -u user -p pwd -s\n -s = silence (no stdout) for cron"
}

run() {
	notes=`wget -q -O - --http-user=${user} --http-passwd=${passwd} ${host}/list_alarm`
	for note in $notes;
	  do
	  wget -q -O - --http-user=${user} --http-passwd=${passwd} ${note}/send_alarm?silence=$1
	done
}

silence=0

while true
do
  case $1 in
	  -h) host=$2
		  shift 2
		  ;;
	  -u) user=$2
		  shift 2
		  ;;
	  -p) passwd=$2
		  shift 2
		  ;;
	  -s) silence=1
		  shift
		  ;;
	  *)
		  break
		  ;;
	  esac
done

if [ -z "$host" -o -z "$user" -o -z "$passwd" ] 
then
	usage
	exit 1
fi

if [ -f $LOCK ] ; then 
	echo -e "Lock file exists : last send_alarm not finished.\nAbord !";
else
	touch $LOCK
	run $silence
	rm -rf $LOCK
fi
