RPMDEFINES := --define "_sourcedir $(SRCDIR)" \
              --define "_specdir $(SRCDIR)" \
              --define "_srcrpmdir $(SRCDIR)" \
              --define "_rpmdir $(SRCDIR)"

SRCDEFINES := --define "dist .remi" \
              --define "_source_filedigest_algorithm 1" \
              --define "_binary_filedigest_algorithm 1"

arch:
	mv *.src.rpm /data/rpms/SRPMS.remi/ && echo done || echo Nothing to do

clean:
	@echo Clean $(NAME) in $(SRCDIR)
	@rm -rfv *~ noarch x86_64 *.src.rpm

srpm:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME).spec

devsrpm:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) -bs $(NAME)-dev.spec

build53:
	time rpmbuild $(RPMDEFINES) --define "phpname php53" --define "runselftest 0" -bb $(NAME).spec

bi53:
	time rpmbuild $(RPMDEFINES) --define "phpname php53" --define "runselftest 0"  -bi --short-circuit  $(NAME).spec

srpm53:
	rpmbuild $(RPMDEFINES) $(SRCDEFINES) --define "phpname php53" -bs $(NAME).spec

build:
	time rpmbuild $(RPMDEFINES) -bb $(NAME).spec

buildmini:
	time rpmbuild $(RPMDEFINES) --define "runselftest 0" -bb $(NAME).spec

bp:
	rpmbuild $(RPMDEFINES) -bp $(NAME).spec

bc:
	rpmbuild $(RPMDEFINES) -bc --short-circuit $(NAME).spec

bi:
	rpmbuild $(RPMDEFINES) -bi --short-circuit $(NAME).spec

devbp:
	rpmbuild $(RPMDEFINES)  --define "runselftest 0" -bp $(NAME)-dev.spec

devbi:
	rpmbuild $(RPMDEFINES)  --define "runselftest 0" -bi --short-circuit $(NAME)-dev.spec

devbl:
	rpmbuild $(RPMDEFINES) -bl --short-circuit $(NAME)-dev.spec

bl:
	rpmbuild $(RPMDEFINES) -bl --short-circuit $(NAME).spec

devbuild:
	time rpmbuild $(RPMDEFINES) -bb $(NAME)-dev.spec

devbuildmini:
	time rpmbuild $(RPMDEFINES) --define "runselftest 0" -bb $(NAME)-dev.spec

sign:
	rpmsign --addsign *.src.rpm

