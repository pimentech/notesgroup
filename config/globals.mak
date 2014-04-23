APPLICATION=notesgroup

ROOTDIR=/home/${CRONUSER}
CONFIGDIR=${ROOTDIR}/config
APACHECONFDIR=${ROOTDIR}/apache
TEMPLATESDIR=${ROOTDIR}/django_templates
STATICDIR=${ROOTDIR}/public_html/${APPLICATION}
LOGDIR=${ROOTDIR}/log
LOGFILE=${LOGDIR}/${APPLICATION}.log

BINDIR=${ROOTDIR}/bin

ADMINDIR=${ROOTDIR}/admin
PATH:=${BINDIR}:/usr/local/bin:${PATH}

DJANGO_SETTINGS_MODULE=dj.apache.settings

SITEHOST=notesgroup.pimentech.net
STATICHOST=${SITEHOST}/static
SITEROOTDIR=/var/www/${APPLICATION}
SITECONFIGDIR=${SITEROOTDIR}/config
SITEMEDIADIR=${SITEROOTDIR}/media

DUMPDIR=${ROOTDIR}/dump

MAILFROM=webmaster@pimentech.net

# UTILISE POUR LE SITE INTRANET
SITESTATICDIR=${SITEROOTDIR}

# Pimentech libs
PIMENTECHDIR=${SITEROOTDIR}/pimentech
PIMENTECHJSDIR=${PIMENTECHDIR}/js
PIMENTECHCSSDIR=${PIMENTECHDIR}/css
PIMENTECHIMAGEDIR=${PIMENTECHDIR}/img

NGBASEURL=http://www.pimentech.fr/pimentech/notesgroup

DBNAME=notesgroup2
DBTYPE=pg
DBHOST=paprika
DBUSER=notesgroup
DBPWD=pwnotesgroup75
DBPORT=5432


MAILTO=info@pimentech.net
FSROOTDIR=/var/lib/notesgroup/fs
SMTPHOST=localhost
DEMO=0
SENDMAIL=/usr/sbin/sendmail
HTTPROOTDIR=/var/www
SITEUSER=
MNTDIR=/mnt
REMOTESERVER=
SITECONFIGDIR=/notesgroup/config
INTRANET_HOST=www.pimentech.fr
SITEINTRANETDIR=/notesgroup/intranet
SITEINTRANETCSSDIR=/notesgroup/intranet/css
SITEINTRANETJSDIR=/notesgroup/intranet/js
SITEINTRANETIMAGESDIR=/notesgroup/intranet/images

SITEPIMENTECHDIR=/pimentech

SHELLDIR=/usr/local/notesgroup/shell
PYTHONPATH=/usr/local/notesgroup/config:/usr/local/notesgroup/shell:/usr/local/python
MAILADMIN=info@pimentech.net

