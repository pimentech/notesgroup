include ../../rules/make.rules
include ../../config/globals.mak

all: 

install: all install-css install-img install-js

install-js: 
	@echo "Installing js files"; cd js && make install

install-img: ${SITESTATICDIR}/img/
	@echo "Installing img files"
	@rsync -ar --cvs-exclude img/ ${SITESTATICDIR}/img/

install-css: ${SITESTATICDIR}/css/
	@echo "Installing css files";cd css && make install

${SITESTATICDIR}/img:
	@echo "doing $@"
	@mkdir -p $@

${SITESTATICDIR}/css:
	@echo "doing $@"
	@mkdir -p $@

