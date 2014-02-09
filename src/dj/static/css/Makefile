include ../../../rules/make.rules
include ../../../config/globals.mak

FILES = intra.css jquery-ui.custom.css final.css
UNCOMPRESSED = minimal.css

notesgroup.css: ${FILES} 
	@echo "doing $@"
	@cat $^ > $@

notesgroup.min.css: notesgroup.css
	@echo "doing $@"
	@cat $< | java -jar ../js/yuicompressor-2.4.2.jar --charset UTF-8 --type css > $@

install.ok: notesgroup.min.css tinymce.css
	@echo "installing $<"
	cp $< ${SITESTATICDIR}/css/
	cp ${UNCOMPRESSED} ${SITESTATICDIR}/css/
	cp tinymce.css ${SITESTATICDIR}/css/
	date > $@

install: install.ok
	@echo "$@ done"

clean:
	@rm -f notesgroup*.css

