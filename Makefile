MOLECULE_ROLES := $(sort $(patsubst roles/%/molecule/default/molecule.yml,%,$(wildcard roles/*/molecule/default/molecule.yml)))

# --all by default so extra scenarios (e.g. aws/upgrade) are never silently
# skipped; narrowed to one scenario only when the caller names it on the
# command line (SCENARIO ?= default can't tell "passed default" from "unset").
SCENARIO ?= default
MOLECULE_TEST_SCOPE := $(if $(filter command line,$(origin SCENARIO)),-s $(SCENARIO),--all)

.PHONY: test converge verify destroy

test:
ifdef ROLE
	cd roles/$(ROLE) && molecule test $(MOLECULE_TEST_SCOPE)
else
	@passed=""; failed=""; \
	for role in $(MOLECULE_ROLES); do \
		echo "==> Testing role: $$role"; \
		if (cd roles/$$role && molecule test --all); then \
			passed="$$passed $$role"; \
		else \
			failed="$$failed $$role"; \
		fi; \
	done; \
	echo ""; \
	echo "========== Summary =========="; \
	total=0; pass_count=0; fail_count=0; \
	for r in $$passed; do total=$$((total+1)); pass_count=$$((pass_count+1)); done; \
	for r in $$failed; do total=$$((total+1)); fail_count=$$((fail_count+1)); done; \
	echo "Total: $$total  Passed: $$pass_count  Failed: $$fail_count"; \
	if [ -n "$$failed" ]; then \
		echo "Failed roles:$$failed"; \
		exit 1; \
	else \
		echo "All roles passed."; \
	fi
endif

converge:
ifndef ROLE
	$(error ROLE is required for converge, e.g. make converge ROLE=github-cli)
endif
	cd roles/$(ROLE) && molecule converge -s $(SCENARIO)

verify:
ifndef ROLE
	$(error ROLE is required for verify, e.g. make verify ROLE=github-cli)
endif
	cd roles/$(ROLE) && molecule verify -s $(SCENARIO)

destroy:
ifndef ROLE
	$(error ROLE is required for destroy, e.g. make destroy ROLE=github-cli)
endif
	cd roles/$(ROLE) && molecule destroy -s $(SCENARIO)
