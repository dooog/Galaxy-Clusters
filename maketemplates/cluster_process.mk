include $(RAWBASEDIR)/maketemplates/master.mk
MAKES = $(shell echo $(patsubst %,%/Makefile,$(wildcard *_*_*_*_*)))
NEDSHIFTS = $(shell echo $(patsubst %,%/nedshifts.tsv,$(wildcard *_*_*_*_*)))
XMM_MAKES = $(shell echo $(patsubst %,%/XMM/Makefile,$(wildcard *_*_*_*_*)))
CHANDRA_MAKES = $(shell echo $(patsubst %,%/chandra/Makefile,$(wildcard *_*_*_*_*)))

.PHONY : all makes nedshifts analyze clean

all : galaxy-clusters-according-to-ned.txt

clean :
	rm -f *.txt

hits.txt :
	find . -iname "*.tsv" -exec wc -l '{}' \; | sort -nr > $@

makes : $(MAKES)

nedshifts : $(NEDSHIFTS)

%/XMM/Makefile: %/Makefile
	make -C $(dir $<) XMM/Makefile

%/chandra/Makefile: %/Makefile
	make -C $(dir $<) chandra/Makefile

%/Makefile:
	echo RAWBASEDIR=$(RAWBASEDIR)/.. > $@
	echo include '$$(RAWBASEDIR)'/maketemplates/analyze.mk >> $@

%/nedshifts.tsv : %/Makefile
	$(MAKE) -C $(dir $@) $(notdir $@)
	touch $@

galaxy-clusters-according-to-ned.txt : $(NEDSHIFTS)
	$(BASEDIR)/bin/chronicle_galaxy_clusters_according_to_ned.sh $(LOWEST_Z) $(HIGHEST_Z) $(CLSTR_SZ) . | sort -nr > $@

galaxy-clusters.txt : $(NEDSHIFTS)
	$(BASEDIR)/bin/chronicle_galaxy_clusters.sh . | sort -nr > $@

analyze : galaxy-clusters-according-to-ned.txt $(MAKES) $(CHANDRA_MAKES) $(XMM_MAKES)
	@for i in `cut -f2 $<` ; do \
		echo make -C `dirname $$i`/XMM ; \
		make -C `dirname $$i`/XMM ; \
	done
