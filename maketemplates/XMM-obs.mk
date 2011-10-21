include $(RAWBASEDIR)/maketemplates/master.mk

all : 

%/Makefile : %
	        echo FIXME > $@

% :
	$(eval OBSURL := $(shell $(PYTHON) $(BASEDIR)/bin/get_XMM_obs_url.py $@))
	@if [ $(OBSURL) ]  ; then \
		if [ $(shell echo $(OBSURL) | grep odf) ] ; then \
			echo ">>>OBSERVATION INCOMPLETE; ONLY ODF AVAILABLE<<<" ; \
			echo ">>>RETRIEVING $(OBSURL) to $(shell pwd)/$@/odf/$(notdir $(OBSURL))<<<" ; \
			mkdir -p $@/odf ; \
			curl $(OBSURL) > $@/odf/$(notdir $(OBSURL)) ; \
		else \
			echo ">>>RETRIEVING $(OBSURL) to $(shell pwd)/$@<<<" ; \
			curl $(OBSURL) | tar x ; \
		fi \
	else \
		echo ">>>COULD NOT GET URL FOR OBSID \"$@\"<<<" ; \
		echo "[SEE $(BASEDIR)/Data/XMM-obs/XSA-logs/$@.html for details]" ; \
	fi
