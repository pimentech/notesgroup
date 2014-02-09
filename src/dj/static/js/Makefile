include ../../../rules/make.rules
include ../../../config/globals.mak

FILES = jquery.dj.js app.js controllers.js
JSTOCHECK = jquery.dj.js

JSCHECKED = ${JSTOCHECK:.js=.ok}

TO_INSTALL = ${HOME}/src/scripts/src/js/jquery.js ${HOME}/src/scripts/src/js/jquery-ui.js jquery.tooltip.js ${HOME}/src/scripts/src/js/jquery.form.js ${HOME}/src/scripts/src/js/jquery.jframe.js ${HOME}/src/scripts/src/lib/tiny_mce/jquery.tinymce.js $ ${HOME}/src/scripts/src/js/jquery.treeview.pack.js  ${FILES}

all: prepare ${JSCHECKED} build/lib.min.js

build/lib.js: ${TO_INSTALL}
	@echo "doing $@"
	@cat $^ > $@

build/lib.min.js: build/lib.js
	@echo "doing $@"
	@cat $< | java -jar yuicompressor-2.4.2.jar --charset UTF-8 --type js > $@.tmp
	@mv -f $@.tmp $@
#	@cp $@ $$(md5sum $@|cut -d" " -f1).$@

install.ok: build/lib.min.js ${SITESTATICDIR}/js
	@echo "installing build/lib.min.js"
	@cp build/lib.min.js ${SITESTATICDIR}/js/
	@date > $@

install: all install.ok
	@echo "$@ done"

clean:
	@rm -f build/lib.min.js build/lib.js *.ok

${SITESTATICDIR}/js:
	@echo "doing $@"
	@mkdir -p $@

prepare:
	@mkdir -p build
